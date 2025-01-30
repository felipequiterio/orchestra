from typing import Dict, Any
from orchestra.core.agent import ToolAgent, AgentTask
# from pydantic import Field



# Example use of how the agent should be ideally defined from ToolAgent
class ToDoAgent(ToolAgent):
    name: str = "Todo Agent"
    description: str = (
        "You are a todo manager responsible for managing todo items and lists"
    )

    # Future decorator to add tools to the agent
    @agent.tool
    def add_task(self, task: Dict) -> Dict:
        return {"status": "success", "message": "Task added successfully"}
    
    @agent.tool
    def update_task(self, task: Dict) -> Dict:
        return {"status": "success", "message": "Task updated successfully"}
    
    @agent.tool
    def delete_task(self, task: Dict) -> Dict:
        return {"status": "success", "message": "Task deleted successfully"}
    
    @agent.tool
    def list_tasks(self, task: Dict) -> Dict:
        return {"status": "success", "message": "List is empty!"}
    
class WeatherAgent(ToolAgent):
    name: str = "Weather Agent"
    description: str = (
        "You are a weather manager responsible for fetching weather information"
    )

    # Future decorator to add tools to the agent
    @agent.tool
    def fetch_weather(self, city: str) -> Dict:
        temperature = 20
        city = "New York City"
        return {"status": "success", "message": f"Weather in {city} is {temperature} degrees"}
    


# Example use of how the agent should be ideally defined from ToolAgent

agent_handler = AgentHandler()

agent_handler.register(ToDoAgent())
agent_handler.register(WeatherAgent())

# response = orchestra.run(query: "Add 'Buy groceries' to the user's to-do list and also fetch the current weather for New York City")

# Main entrypoint would be the orchestra.run() function, that will recieve the query and return the response from the query execution.

# Inside orchestra.run(), could be something like this:

# def run(query: str) -> Dict[str, Any]:

    # Generate the task list from the query
    # task_list = task.generate_list(query)
    
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
    
    # for task in task_list.steps:
    #     agent = agent_list.get(task.agent)
    #     result = agent.execute(task.task)
    #     results.append(result)
    # return results

    # Example results:
    # {"status": "success", "agent": "todo_agent", "message": "Task added successfully"}
    # {"status": "success", "agent": "weather_agent", "message": "Weather in New York City is 20 degrees"}
