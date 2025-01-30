from typing import List, Optional, Dict
from pydantic import BaseModel
from .agent import ToolAgent
from ..utils.logger import get_logger

logger = get_logger(__name__)


class AgentHandler(BaseModel):
    """Manages agent registration and retrieval"""

    agents: Dict[str, ToolAgent] = {}

    def register(self, agent: ToolAgent) -> None:
        """Register a new agent"""
        logger.info(f"Registering agent: {agent.name}")
        if agent.name in self.agents:
            logger.warning(f"Agent {agent.name} already registered, updating...")
        self.agents[agent.name] = agent

    def get_agent(self, name: str) -> Optional[ToolAgent]:
        """Retrieve an agent by name"""
        return self.agents.get(name)

    def list_agents(self) -> List[ToolAgent]:
        """List all registered agents"""
        return list(self.agents.values())

    def remove_agent(self, name: str) -> None:
        """Remove an agent from the registry"""
        if name in self.agents:
            logger.info(f"Removing agent: {name}")
            del self.agents[name]
