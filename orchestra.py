# Inside orchestra.run(), could be something like this:

def run(query: str, agent_list: List[BaseAgent] = None, task_list: List[Task] = None) -> Dict[str, Any]:

    # Generate the task list from the query
    if task_list is None:
        task_list = task.generate_list(query)
    
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
    
    for task in task_list.steps:
        agent = agent_list.get(task.agent)
        result = agent.execute(task.task)
        results.append(result)
    return results

    # Example results:
    # {"status": "success", "agent": "todo_agent", "message": "Task added successfully"}
    # {"status": "success", "agent": "weather_agent", "message": "Weather in New York City is 20 degrees"}
