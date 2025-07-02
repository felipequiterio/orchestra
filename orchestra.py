import core.task as task
from core.agent import BaseAgent
from core.task import Task, TaskList
from typing import List, Any, Dict
import json

def run(query: str, agent_list: List[BaseAgent], task_list: TaskList = None) -> str:
    """
    Main entry point for Orchestra framework.
    
    Args:
        query: The user's query to process
        agent_list: List of available agents
        task_list: Optional pre-defined task list (if None, will be generated automatically)
    
    Returns:
        Final synthesized answer as a string
    """
    # Generate the task list from the query
    if task_list is None:
        task_list = task.generate(query, agent_list)
    
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
    print("\n" + "="*60)
    print("🎯 TASK EXECUTION RESULTS")
    print("="*60)
    
    for i, result in enumerate(results, 1):
        status = result.get('status', 'unknown')
        step = result.get('step', 'N/A')
        is_async = result.get('is_async', False)
        
        # Status emoji and color coding
        status_emoji = "✅" if status == 'success' else "❌" if status == 'error' else "❓"
        status_text = f"{status_emoji} {status.upper()}"
        
        print(f"\n{'🔄' if is_async else '⚡'} Task {i} (Step {step})")
        print(f"Status: {status_text}")
        
        # Add task description from the original task list
        if task_list and step != 'N/A':
            # Find the corresponding task in the task list
            for task_item in task_list.steps:
                if task_item.step_number == step:
                    print(f"Task: {task_item.task}")
                    break
        
        if status == 'success':
            result_data = result.get('result', {})
            if isinstance(result_data, dict):
                # Extract key information for cleaner display
                if 'tool_used' in result_data:
                    print(f"Tool: {result_data['tool_used']}")
                if 'result' in result_data and isinstance(result_data['result'], dict):
                    if 'message' in result_data['result']:
                        print(f"Output: {result_data['result']['message']}")
                    elif 'data' in result_data['result']:
                        print(f"Data: {result_data['result']['data']}")
                else:
                    print(f"Result: {result_data}")
            else:
                print(f"Result: {result_data}")
        else:
            print(f"Error: {result.get('message', 'Unknown error')}")
            
        if is_async:
            print("⏱️  (Async execution)")
    
    print("="*60)

    # Example results:
    # {"status": "success", "agent": "todo_agent", "message": "Task added successfully"}
    # {"status": "success", "agent": "weather_agent", "message": "Weather in New York City is 20 degrees"}
    
    final_answer = task.generate_final_answer(query, results)
    return final_answer


