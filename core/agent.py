import os
import sys
from abc import ABC, abstractmethod
from typing import Any, Dict, List

from pydantic import BaseModel, Field

import json

from orchestra.core.tools import Tool
from orchestra.core.events import events, Event, EventType
from orchestra.llm.base import model_invoke
import sys as _sys

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

    # @abstractmethod
    # async def execute_async(self, task: AgentTask) -> Dict[str, Any]:
    #     """Execute a task asynchronously and return the results"""

    #     pass


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
        
        events.emit(Event(
            type=EventType.AGENT_START,
            source=self.name,
            data={"task": task.task, "expected_output": task.expected_output}
        ))

        tools_schema = {
            "type": "object",
            "properties": {
                "tool_execution": {
                    "type": "object",
                    "properties": {
                        "tool_name": {
                            "type": "string",
                            "enum": [tool.name for tool in self.tools],
                            "description": "The name of the tool to use",
                        },
                        "tool_args": {
                            "type": "object",
                            "description": "The arguments for the selected tool",
                        },
                    },
                    "required": ["tool_name", "tool_args"],
                },
                "reasoning": {
                    "type": "string",
                    "description": "Explanation for the tool choice and argument values",
                },
            },
            "required": ["tool_execution", "reasoning"],
        }

        user_message = (
            f"Your task is to complete the following objective as an expert agent.\n"
            f"\n"
            f"Task:\n{task.task}\n"
            f"\n"
            f"Expected Output:\n{task.expected_output}\n"
            f"\n"
            f"You have access to the following tools. Each tool has a name, a description, and a set of parameters you must provide as arguments:\n"
            f"{json.dumps([tool.get_schema() for tool in self.tools], indent=2)}\n"
            f"\n"
            f"Instructions:\n"
            f"- Carefully review the available tools and their parameters.\n"
            f"- Select the single most appropriate tool to accomplish the task.\n"
            f"- Provide the tool name and a dictionary of arguments (with values) for the tool's parameters.\n"
            f"- Justify your tool selection and argument choices with clear reasoning.\n"
            f"\n"
            f"Respond ONLY in the following JSON format:\n"
            f"{{\n"
            f'  "tool_execution": {{\n'
            f'    "tool_name": "<tool name>",\n'
            f'    "tool_args": {{ "<param1>": <value1>, ... }}\n'
            f"  }},\n"
            f'  "reasoning": "<your explanation>"\n'
            f"}}\n"
        )

        response = model_invoke(
            system_message=self.system_prompt,
            user_message=user_message,
            payload=tools_schema,
            model=self.model,
        )

        # Handle different response formats
        if "tool_execution" in response:
            # Expected format with explicit tool selection and arguments
            selected_tool = next(
                (
                    tool
                    for tool in self.tools
                    if tool.name == response["tool_execution"]["tool_name"]
                ),
                None,
            )

            if not selected_tool:
                raise ValueError(
                    f"Selected tool '{response['tool_execution']['tool_name']}' not found"
                )

            tool_args = response["tool_execution"]["tool_args"]
            reasoning = response.get("reasoning", "")

        else:
            # Try to intelligently match the response to a tool based on parameter names
            best_match_tool = None
            best_match_score = 0
            
            for tool in self.tools:
                tool_schema = tool.get_schema()
                tool_params = tool_schema.get('parameters', {}).get('properties', {})
                
                if isinstance(response, dict):
                    if len(tool_params) == 0:
                        # For tools with no parameters, check if response is empty or has no meaningful parameters
                        if not response or all(v is None or v == '' for v in response.values()):
                            match_score = 1.0  # Perfect match for parameterless tools with empty response
                            if match_score > best_match_score:
                                best_match_score = match_score
                                best_match_tool = tool
                    else:
                        # Count how many response keys match tool parameters
                        matching_params = sum(1 for key in response.keys() if key in tool_params)
                        match_score = matching_params / len(tool_params) if tool_params else 0
                        
                        if match_score > best_match_score and matching_params > 0:
                            best_match_score = match_score
                            best_match_tool = tool

            if best_match_tool:
                selected_tool = best_match_tool
                tool_args = response if len(selected_tool.get_schema().get('parameters', {}).get('properties', {})) > 0 else {}
                reasoning = f"Intelligently selected {selected_tool.name} based on parameter matching (score: {best_match_score:.2f})"
            elif len(self.tools) == 1:
                # Fallback: single tool available
                selected_tool = self.tools[0]
                tool_args = response
                reasoning = "Automatically selected tool based on single available option."
            else:
                raise ValueError(
                    "Response format unrecognized and multiple tools are available; cannot determine tool to execute."
                )

        events.emit(Event(
            type=EventType.TOOL_SELECTION,
            source=self.name,
            data={
                "tool": selected_tool.name,
                "arguments": tool_args,
                "reasoning": reasoning
            }
        ))

        # Execute the selected tool with provided arguments
        try:
            events.emit(Event(
                type=EventType.TOOL_START,
                source=self.name,
                data={"tool": selected_tool.name, "arguments": tool_args}
            ))
            
            result = selected_tool.run(**tool_args)
            
            events.emit(Event(
                type=EventType.TOOL_END,
                source=self.name,
                data={"tool": selected_tool.name, "result": result}
            ))
            
            output = {
                "result": result,
                "tool_used": selected_tool.name,
                "reasoning": reasoning,
                "arguments": tool_args,
            }
            
            events.emit(Event(
                type=EventType.AGENT_END,
                source=self.name,
                data={"output": output}
            ))
            
            return output

        except Exception as e:
            events.emit(Event(
                type=EventType.TOOL_ERROR,
                source=self.name,
                data={"tool": selected_tool.name, "error": str(e)}
            ))
            raise ValueError(f"Tool execution failed: {str(e)}")

    # @abstractmethod
    # async def execute_async(self, task: AgentTask) -> Dict[str, Any]:
    #     """Execute a task asynchronously and return the results"""
    #     pass


agent = _sys.modules[__name__]