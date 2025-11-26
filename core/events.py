import asyncio
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, List
from pydantic import BaseModel, Field

class EventType(str, Enum):
    # Orchestra lifecycle
    ORCHESTRA_START = "orchestra_start"
    ORCHESTRA_END = "orchestra_end"
    
    # Task Planning
    TASK_GENERATION_START = "task_generation_start"
    TASK_GENERATION_END = "task_generation_end"
    
    # Task Execution
    TASK_START = "task_start"
    TASK_COMPLETE = "task_complete"
    TASK_ERROR = "task_error"
    
    # Agent lifecycle
    AGENT_START = "agent_start"
    AGENT_END = "agent_end"
    
    # Tool usage
    TOOL_SELECTION = "tool_selection"
    TOOL_START = "tool_start"
    TOOL_END = "tool_end"
    TOOL_ERROR = "tool_error"
    
    # General
    LOG = "log"

class Event(BaseModel):
    type: EventType
    source: str = Field(..., description="Component source of the event (e.g., 'orchestra', 'weather_agent')")
    data: Dict[str, Any] = Field(default_factory=dict, description="Event payload")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class EventBus:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EventBus, cls).__new__(cls)
            cls._instance._subscribers = []
        return cls._instance
    
    def __init__(self):
        # Singleton initialization handles this, but typing needs it
        if not hasattr(self, "_subscribers"):
            self._subscribers: List[Callable[[Event], Any]] = []

    def subscribe(self, callback: Callable[[Event], Any]):
        """Add a listener for events"""
        self._subscribers.append(callback)
        
    def unsubscribe(self, callback: Callable[[Event], Any]):
        """Remove a listener"""
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    def emit(self, event: Event):
        """Emit an event to all subscribers"""
        # Synchronous execution of callbacks for now
        # In a full async setup, we might want to await these if they are coroutines
        for callback in self._subscribers:
            try:
                if asyncio.iscoroutinefunction(callback):
                    # If we are in an event loop, schedule it, otherwise run it?
                    # For now, Orchestra seems synchronous in parts, so we'll assume sync callbacks primarily
                    # or fire-and-forget for async ones if we had a running loop available easily here.
                    # Given the current structure, let's keep it simple.
                    pass 
                
                # Check if the callback expects arguments
                callback(event)
            except Exception as e:
                print(f"Error in event subscriber: {e}")

    def reset(self):
        """Clear all subscribers"""
        self._subscribers = []

# Global instance
events = EventBus()

