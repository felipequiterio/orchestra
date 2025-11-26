from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: float = Field(default_factory=lambda: __import__("time").time())

class OrchestraContext(BaseModel):
    """
    Holds the context for the current execution, including conversation history.
    """
    session_id: str = "default"
    history: List[ChatMessage] = Field(default_factory=list)

    def add_message(self, role: MessageRole, content: str):
        self.history.append(ChatMessage(role=role, content=content))

    def get_formatted_history(self, limit: int = 10) -> str:
        """
        Returns the chat history formatted as a string for the LLM prompt.
        Limits to the last N messages to save tokens.
        """
        if not self.history:
            return "No previous conversation history."

        formatted = []
        # Take the last 'limit' messages
        recent_history = self.history[-limit:]
        
        for msg in recent_history:
            role_name = "User" if msg.role == MessageRole.USER else "Assistant"
            formatted.append(f"{role_name}: {msg.content}")
            
        return "\n".join(formatted)

    def clear(self):
        self.history = []

