from typing import Dict, Any
from core.agent import ToolAgent, AgentTask



class WeatherAgent(ToolAgent):
    """Mock weather agent for testing"""
    
    name: str = "weather_agent"
    description: str = "Fetches weather information for locations"
    system_prompt: str = "You are a weather information assistant that provides weather data for different locations."
    
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
    system_prompt: str = "You are a todo list manager that helps users manage their tasks and todo items."
    
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