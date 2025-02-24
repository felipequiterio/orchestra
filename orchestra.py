import core.task as task
from core.agent import BaseAgent
from core.task import Task
from typing import List, Any, Dict

def run(query: str, agent_list: List[BaseAgent], task_list: List[Task] = None) -> Dict[str, Any]:

    # Generate the task list from the query
    if task_list is None:
        task_list = task.generate_list(query)
    
    if agent_list is None:
        raise ValueError("Agent list is required")
    
    # Example task_list:
    # [
#     {
#         "step_number": 1,
#         "task": "Add 'Buy groceries' to the user's to-do list",
#         "agent": "todo_agent",
#         "expected_output": "Confirmation that 'Buy groceries' was added to the to-do list",
#         "is_async": true
#     },
#     {
#         "step_number": 2,
#         "task": "Fetch the current weather for New York City",
#         "agent": "weather_agent",
#         "expected_output": "Current weather conditions in New York City",
#         "is_async": false
#     },
#   ]

    # Then, match the task_list with the agents and execute the tasks
    results = task.route(task_list, agent_list)

    # Example results:
    # {"status": "success", "agent": "todo_agent", "message": "Task added successfully"}
    # {"status": "success", "agent": "weather_agent", "message": "Weather in New York City is 20 degrees"}
    
    final_answer = task.generate_final_answer(query, results)
    return final_answer


