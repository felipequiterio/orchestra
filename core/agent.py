from abc import ABC, abstractmethod
from typing import Dict, Any
from pydantic import BaseModel, Field


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

    @abstractmethod
    def execute(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a task and return the results"""
        pass

    @abstractmethod
    async def execute_async(self, task: AgentTask) -> Dict[str, Any]:
        """Execute a task asynchronously and return the results"""
        pass


