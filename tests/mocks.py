from typing import Dict, Any, List, Optional
from core.agent import ToolAgent, AgentTask
from core.task import TaskList, Task
from core.tools import Tool

class WeatherTool(Tool):
    name: str = "get_weather"
    description: str = "Get weather information for a location"
    
    def run(self, location: str, units: Optional[str] = "celsius") -> str:
        """Get weather information for a specific location.
        
        Args:
            location: The city or location to get weather for
            units: Temperature units (celsius/fahrenheit)
        
        Returns:
            Weather information as a string
        """
        return f"Weather in {location} is sunny and 25°{units}"

class TodoTool(Tool):
    name: str = "manage_todo"
    description: str = "Manage todo items and lists"
    
    def run(self, action: str, task: Optional[str] = None) -> Dict[str, Any]:
        """Manage todo list items.
        
        Args:
            action: The action to perform (add/remove/list/update)
            task: The task description to manage
        
        Returns:
            Status and updated todo list
        """
        return {
            "status": "success",
            "message": f"Task '{task}' {action}ed successfully",
            "tasks": ["Buy groceries", "Walk the dog"]
        }

# Initialize tool instances
weather_tool = WeatherTool()
todo_tool = TodoTool()

# Test tasks
task_1 = Task(
    step_number=1,
    task="Get the weather in New York",
    agent="weather_agent",
    expected_output="The weather in New York",
    is_async=False
)

task_2 = Task(
    step_number=2,
    task="Add 'Buy groceries' to the user's to-do list",
    agent="todo_agent",
    expected_output="The task 'Buy groceries' has been added to the user's to-do list",
    is_async=False
)

task_list = TaskList(
    steps=[task_1, task_2]
)

class WeatherAgent(ToolAgent):
    """Mock weather agent for testing"""
    
    name: str = "weather_agent"
    description: str = "Fetches weather information for locations"
    backstory: str = "I am a weather agent that has been helping people check the weather since 2024"
    system_prompt: str = "You are a weather information assistant that provides weather data for different locations."
    tools: List[Tool] = [weather_tool]
    model: str = "gpt-3.5-turbo"
    
    input_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location to get weather for"
            }
        },
        "required": ["location"]
    }
    
    output_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "temperature": {"type": "number"},
            "conditions": {"type": "string"},
            "location": {"type": "string"}
        },
        "required": ["temperature", "conditions", "location"]
    }

    def execute(self, task: AgentTask) -> Dict[str, Any]:
        """Mock weather data return"""
        return {
            "temperature": 72,
            "conditions": "sunny",
            "location": "New York"
        }

    async def execute_async(self, task: AgentTask) -> Dict[str, Any]:
        """Mock async weather data return"""
        return await self.execute(task)


class TodoAgent(ToolAgent):
    """Mock todo list agent for testing"""
    
    name: str = "todo_agent"
    description: str = "Manages todo items and lists"
    backstory: str = "I am a todo list manager that has been helping people stay organized since 2024"
    system_prompt: str = "You are a todo list manager that helps users manage their tasks and todo items."
    tools: List[Tool] = [todo_tool]
    model: str = "ollama"
    
    input_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["add", "remove", "list", "update"],
                "description": "The action to perform"
            },
            "task": {
                "type": "string",
                "description": "The task description"
            }
        },
        "required": ["action"]
    }
    
    output_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "message": {"type": "string"},
            "tasks": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["status", "message"]
    }

    def execute(self, task: AgentTask) -> Dict[str, Any]:
        """Mock todo operation return"""
        return {
            "status": "success",
            "message": "Task processed successfully",
            "tasks": ["Buy groceries", "Walk the dog"]
        }

    async def execute_async(self, task: AgentTask) -> Dict[str, Any]:
        """Mock async todo operation return"""
        return await self.execute(task)
    
    
agent_list = [
    WeatherAgent(),
    TodoAgent()
]