#!/usr/bin/env python3
"""
Example usage of the Orchestra framework.

This example demonstrates:
1. Creating custom tools
2. Creating custom agents
3. Using the Orchestra framework to orchestrate tasks
4. Handling both simple and complex multi-step queries
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, List

# Add the parent directory to the path to import orchestra modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from orchestra import run
from core.agent import ToolAgent, AgentTask
from core.tools import Tool


# ============================================================================
# Custom Tools
# ============================================================================

class WeatherTool(Tool):
    """Tool for getting weather information"""
    
    name: str = "get_weather"
    description: str = "Get current weather information for a specific city"
    
    def run(self, city: str, country: str = "US") -> Dict[str, Any]:
        """
        Get weather information for a city.
        
        Args:
            city: The city name
            country: The country code (default: US)
        """
        # Simulate weather data - in a real implementation, this would call a weather API
        weather_data = {
            "city": city,
            "country": country,
            "temperature": 22,
            "condition": "Sunny",
            "humidity": 65,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "status": "success",
            "data": weather_data,
            "message": f"Weather in {city}, {country}: {weather_data['temperature']}°C, {weather_data['condition']}"
        }


class TodoTool(Tool):
    """Tool for managing todo items"""
    
    name: str = "manage_todo"
    description: str = "Add, remove, or list todo items"
    
    def run(self, action: str, item: str = None) -> Dict[str, Any]:
        """
        Manage todo items.
        
        Args:
            action: The action to perform (add, remove, list)
            item: The todo item (required for add/remove actions)
        """
        # Simulate todo storage - in a real implementation, this would use a database
        if not hasattr(self, '_todos'):
            self._todos = []
        
        if action == "add":
            if not item:
                return {"status": "error", "message": "Item is required for add action"}
            self._todos.append({"item": item, "created": datetime.now().isoformat()})
            return {"status": "success", "message": f"Added '{item}' to todo list", "todos": self._todos}
        
        elif action == "remove":
            if not item:
                return {"status": "error", "message": "Item is required for remove action"}
            for todo in self._todos:
                if todo["item"] == item:
                    self._todos.remove(todo)
                    return {"status": "success", "message": f"Removed '{item}' from todo list", "todos": self._todos}
            return {"status": "error", "message": f"Item '{item}' not found in todo list"}
        
        elif action == "list":
            return {"status": "success", "message": "Current todo items", "todos": self._todos}
        
        else:
            return {"status": "error", "message": f"Invalid action: {action}. Use 'add', 'remove', or 'list'"}


class CalculatorTool(Tool):
    """Tool for performing mathematical calculations"""
    
    name: str = "calculate"
    description: str = "Perform mathematical calculations"
    
    def run(self, expression: str) -> Dict[str, Any]:
        """
        Perform mathematical calculations using eval.
        
        Args:
            expression: The mathematical expression to evaluate (e.g., "2 + 3", "10 ** 2", "sqrt(16)")
        """
        try:
            # Define safe math functions
            import math
            safe_dict = {
                'abs': abs, 'round': round, 'min': min, 'max': max,
                'sqrt': math.sqrt, 'pow': pow, 'sin': math.sin, 'cos': math.cos,
                'tan': math.tan, 'log': math.log, 'exp': math.exp
            }
            
            # Evaluate the expression safely
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            
            return {
                "status": "success",
                "result": result,
                "expression": expression
            }
        
        except ZeroDivisionError:
            return {"status": "error", "message": "Division by zero is not allowed"}
        except ValueError as e:
            return {"status": "error", "message": f"Invalid mathematical operation: {str(e)}"}
        except Exception as e:
            return {"status": "error", "message": f"Calculation error: {str(e)}"}


# ============================================================================
# Custom Agents
# ============================================================================

class WeatherAgent(ToolAgent):
    """Agent specialized in weather-related tasks"""
    
    name: str = "weather_agent"
    description: str = "Specialized agent for weather-related queries and tasks"
    backstory: str = "I am a weather expert agent with access to real-time weather data and forecasting capabilities."
    system_prompt: str = """
    You are a weather expert agent. Your role is to:
    1. Understand weather-related queries
    2. Use the weather tool to fetch current weather information
    3. Provide clear, accurate weather reports
    4. Handle weather-related calculations and comparisons
    
    Always use the available weather tools to get the most current information.
    """
    input_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "city": {"type": "string", "description": "City name"},
            "country": {"type": "string", "description": "Country code"}
        }
    }
    output_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "weather_info": {"type": "object", "description": "Weather information"},
            "summary": {"type": "string", "description": "Weather summary"}
        }
    }
    tools: List[Tool] = [WeatherTool()]
    model: str = "ollama"
    
    async def execute_async(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a task asynchronously"""
        return self.execute(task)


class TodoAgent(ToolAgent):
    """Agent specialized in todo management tasks"""
    
    name: str = "todo_agent"
    description: str = "Specialized agent for managing todo lists and tasks"
    backstory: str = "I am a productivity agent that helps users manage their todo lists efficiently."
    system_prompt: str = """
    You are a todo management expert agent. Your role is to:
    1. Understand todo-related requests
    2. Use the todo tool to add, remove, or list items
    3. Provide clear confirmations and status updates
    4. Help organize and prioritize tasks
    
    Always use the available todo tools to manage the user's todo list.
    """
    input_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "action": {"type": "string", "description": "Action to perform (add, remove, list)"},
            "item": {"type": "string", "description": "Todo item"}
        }
    }
    output_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "action_result": {"type": "object", "description": "Result of the action"},
            "todo_list": {"type": "array", "description": "Current todo list"}
        }
    }
    tools: List[Tool] = [TodoTool()]
    model: str = "ollama"
    
    async def execute_async(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a task asynchronously"""
        return self.execute(task)


class CalculatorAgent(ToolAgent):
    """Agent specialized in mathematical calculations"""
    
    name: str = "calculator_agent"
    description: str = "Specialized agent for mathematical calculations and computations"
    backstory: str = "I am a mathematical computation agent that can perform various calculations accurately."
    system_prompt: str = """
    You are a mathematical computation expert agent. Your role is to:
    1. Understand mathematical queries and expressions
    2. Use the calculator tool to perform accurate calculations
    3. Provide clear explanations of the mathematical operations
    4. Handle complex mathematical problems step by step
    
    Always use the available calculator tools to ensure accuracy.
    """
    input_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "expression": {"type": "string", "description": "Mathematical expression"},
            "operation": {"type": "string", "description": "Mathematical operation"}
        }
    }
    output_schema: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "calculation_result": {"type": "object", "description": "Result of the calculation"},
            "explanation": {"type": "string", "description": "Explanation of the calculation"}
        }
    }
    tools: List[Tool] = [CalculatorTool()]
    model: str = "ollama"
    
    async def execute_async(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a task asynchronously"""
        return self.execute(task)

# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Main function to run all examples"""
    print("Orchestra Framework - Example Usage")
    print("This example demonstrates the Orchestra framework capabilities")
    
    # Run all examples
    agent_list = [WeatherAgent(), TodoAgent(), CalculatorAgent()]
    query = "What's the weather in Tokyo and calculate 15% of 84590? Also add 'Buy groceries' to my todo list."
    response = run(query, agent_list)

    print(f'User query: {query}\n\n')
    print(f'Final response: {response}\n\n')
    print("\nExample completed!")


if __name__ == "__main__":
    main() 