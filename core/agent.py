from abc import ABC, abstractmethod
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from llm.base import model_invoke
from .tools import Tool
import json

class AgentTask(BaseModel):
    """Represents a task to be executed by an agent"""

    task: str = Field(..., description="Task description")
    expected_output: str = Field(..., description="Expected output description")
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Optional task metadata"
    )


class BaseAgent(ABC, BaseModel):
    """Base class for all agents"""
    
    name: str = Field(..., description="Unique name of the agent")
    description: str = Field(..., description="Agent description")
    backstory: str = Field(..., description="Backstory of the agent")
    
    @abstractmethod 
    def execute(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a task and return the results"""
        pass

    @abstractmethod
    async def execute_async(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a task asynchronously and return the results"""
        
        pass


class ToolAgent(BaseAgent):
    """Base class for agents that use specific tools"""

    system_prompt: str = Field(..., description="System prompt for the agent")
    input_schema: Dict[str, Any] = Field(..., description="Input validation schema")
    output_schema: Dict[str, Any] = Field(..., description="Output validation schema")
    tools: List[Tool] = Field(..., description="List of tools available to the agent")
    model: str = Field(..., description="Model to use for the agent")

    def _format_tools(self) -> str:
        """Format the tools for the agent"""
        formatted_tools = []
        for tool in self.tools:
            formatted_tools.append(
                f"-------------------------------\n"
                f"Tool: {tool.name}\n"
                f"Description: {tool.description}\n"
                f"-------------------------------"
            )
        return "\n".join(formatted_tools)
    
    def execute(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a task and return the results"""
        
        tools_schema = {
            "type": "object",
            "properties": {
                "tool_execution": {
                    "type": "object",
                    "properties": {
                        "tool_name": {
                            "type": "string",
                            "enum": [tool.name for tool in self.tools],
                            "description": "The name of the tool to use"
                        },
                        "tool_args": {
                            "type": "object",
                            "description": "The arguments for the selected tool"
                        }
                    },
                    "required": ["tool_name", "tool_args"]
                },
                "reasoning": {
                    "type": "string",
                    "description": "Explanation for the tool choice and argument values"
                }
            },
            "required": ["tool_execution", "reasoning"]
        }
        
        response = model_invoke(
            system_message=self.system_prompt,
            user_message=f"""
                Task: {task.task}
                Expected Output: {task.expected_output}

                Available Tools:
                {json.dumps([tool.get_schema() for tool in self.tools], indent=2)}

                Select a tool and provide its arguments to complete this task.""",
            payload=tools_schema,
            model=self.model
        )
        
        selected_tool = next(
            (tool for tool in self.tools if tool.name == response["tool_execution"]["tool_name"]),
            None
        )
        
        if not selected_tool:
            raise ValueError(f"Selected tool '{response['tool_execution']['tool_name']}' not found")
        
        try:
            result = selected_tool.run(**response["tool_execution"]["tool_args"])
            return {
                "result": result,
                "tool_used": selected_tool.name,
                "reasoning": response["reasoning"],
                "arguments": response["tool_execution"]["tool_args"]
            }
        except Exception as e:
            raise ValueError(f"Tool execution failed: {str(e)}")

    @abstractmethod
    async def execute_async(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a task asynchronously and return the results"""
        pass


