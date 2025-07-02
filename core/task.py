import json
from typing import Dict, List

from pydantic import BaseModel

from core.agent import AgentTask, BaseAgent
from llm.base import model_invoke
from utils.logger import get_custom_logger

logger = get_custom_logger("TASK")

tasks_payload = {
    "name": "route_agent",
    "description": "Route the query to one or multiple agents, handling single or multi-step tasks.",
    "parameters": {
        "type": "object",
        "properties": {
            "steps": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "step_number": {
                            "type": "integer",
                            "description": "The step number of the query (starting from 1)",
                        },
                        "task": {
                            "type": "string",
                            "description": "Task description the agent needs to complete",
                        },
                        "agent": {
                            "type": "string",
                            "description": "The agent responsible for this task",
                        },
                        "expected_output": {
                            "type": "string",
                            "description": "What output is expected after completion of the task",
                        },
                        "is_async": {
                            "type": "boolean",
                            "description": "Whether this task should be performed asynchronously",
                        },
                    },
                    "required": ["step_number", "task", "agent"],
                },
            }
        },
        "required": ["steps"],
    },
}


class Task(BaseModel):
    step_number: int
    task: str
    agent: str
    expected_output: str
    is_async: bool


class TaskList(BaseModel):
    steps: List[Task]


def generate(user_message: str, agent_list: List[BaseAgent]) -> TaskList:
    agents_available = "\n".join(
        [
            f"- **Name**: `{agent.name}`\n  **Description**: {agent.description}"
            for agent in agent_list
        ]
    )

    system = f"""
                You are an intelligent assistant responsible for routing queries to the appropriate agents.
                When a query is simple and can be handled by a single agent, route it directly to that agent with the necessary task information.
                
                For complex queries that require multiple steps or involve multiple agents:
                - Identify each step needed to complete the query. Each step should be a distinct task with a specific goal.
                - Assign a unique `step_number` to each task, starting from 1, indicating the order of execution.
                - Choose the most appropriate `agent` for each task, based on the task's requirements and the agent's capabilities.
                - For tasks that need to be executed asynchronously, set `is_async` to `true`. This will indicate that the task can be completed independently without blocking other tasks.
                - For each task, clearly describe the expected outcome in `expected_output`. This will guide the agent on the form and content of the response.
                
                If a task is complex and requires further subdivision, split it into smaller tasks that can be routed to the same agent or different agents. 
                Provide the complete list of subtasks and the order in which they should be executed.

                Ensure that the output structure follows this format:
                - `steps`: an array containing each task, where each task includes:
                    - `step_number`: the step in the sequence
                    - `task`: a detailed description of the task to be completed
                    - `agent`: the agent designated to handle the task
                    - `expected_output`: a description of what the agent should provide after completing the task
                    - `is_async`: whether this task is asynchronous
                    
                Example:
                [
                    {{
                        "step_number": 1,
                        "task": "Fetch the current weather for New York City",
                        "agent": "weather_agent",
                        "expected_output": "Current weather conditions in New York City",
                        "is_async": false
                    }},
                    {{
                        "step_number": 2,
                        "task": "Add 'Buy groceries' to the user's to-do list",
                        "agent": "todo_agent",
                        "expected_output": "Confirmation that 'Buy groceries' was added to the to-do list",
                        "is_async": true
                    }}
                ]

                Available agents:
                {agents_available}
                """

    # logger.info(f"Sending task generation request with message: {user_message}")

    response = model_invoke(system, user_message, tasks_payload)
    # logger.info(f"Generation response: {response}")

    # Handle both string and dict responses
    if isinstance(response["steps"], str):
        tasks = json.loads(response["steps"])
    else:
        tasks = response["steps"]

    tasks_list = {"steps": tasks}

    tasks_list = TaskList.model_validate(tasks_list)
    # logger.info(f"Successfully validated {len(tasks_list.steps)} tasks")
    # logger.info(f"Task list: {json.dumps(tasks_list.model_dump(), indent=2)}")

    return tasks_list


def route(task_list: TaskList, agent_list: List[BaseAgent]) -> List[Dict]:
    results = []

    available_agents = {}

    for agent in agent_list:
        available_agents[agent.name.lower()] = agent

    # logger.info(f"Available agents: {available_agents}")

    for task in task_list.steps:
        target_agent_name = task.agent.lower()

        if target_agent_name not in available_agents.keys():
            results.append(
                {
                    "step": task.step_number,
                    "status": "error",
                    "result": "None",
                    "message": f"Agent '{target_agent_name}' not found in agent list",
                }
            )
            continue

        agent = available_agents[target_agent_name]
        # logger.info(f"Agent: {agent}")

        agent_task = AgentTask(task=task.task, expected_output=task.expected_output)

        response = agent.execute(agent_task)
        results.append(
            {
                "step": task.step_number,
                "status": "success",
                "result": response,
                "is_async": task.is_async,
            }
        )

    return results


def generate_final_answer(message: str, results: List[Dict]) -> str:
    # Format results for the LLM
    formatted_results = []
    for result in results:
        status = result.get("status", "unknown")
        step = result.get("step", 0)

        if status == "success":
            formatted_results.append(
                f"Task {step}: Success - {result.get('result', {})}"
            )
        else:
            formatted_results.append(
                f"Task {step}: Failed - {result.get('message', 'Unknown error')}"
            )

    results_str = "\n".join(formatted_results)

    system = """
    You are an intelligent assistant tasked with synthesizing results from multiple tasks into a clear, concise final answer.

    Your role is to:
    1. Analyze the results from each completed task
    2. Extract the key information and insights 
    3. Combine them into a coherent response that directly addresses the user's original request
    4. Handle both successful and failed task results appropriately
    5. Present the information in a natural, conversational way
    
    If any tasks failed, acknowledge the failure and explain what information is still available.
    Focus on providing actionable insights and clear conclusions based on the available results.
    """

    user_message = f"""
    Original Request: {message}
    
    Task Results:
    {results_str}
    
    Please provide a natural response that synthesizes these results.
    """

    response = model_invoke(system, user_message, None)
    return response["content"] if isinstance(response, dict) else response
