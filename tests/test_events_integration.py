import sys
import os
import json
from unittest.mock import patch, MagicMock

# No need for sys.path hack if we run from backend/ root or if we rely on standard python behavior
# But to be safe, let's ensure current dir (backend/) is in path if we run it from project root
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from orchestra.core.events import events, EventType
from orchestra.core.agent import ToolAgent
from orchestra.core.tools import Tool
from orchestra.orchestra import run
from orchestra.core.task import TaskList, Task

# Define a simple tool
class EchoTool(Tool):
    name: str = "echo"
    description: str = "Echoes the input"
    def run(self, message: str):
        return f"Echo: {message}"

    def get_schema(self):
        return {
            "name": "echo",
            "description": "Echoes the input",
            "parameters": {
                "type": "object",
                "properties": {
                    "message": {"type": "string"}
                }
            }
        }

# Define a simple agent
class EchoAgent(ToolAgent):
    name: str = "echo_agent"
    description: str = "Echoes things"
    backstory: str = "I echo."
    system_prompt: str = "You echo."
    input_schema: dict = {}
    output_schema: dict = {}
    tools: list = [EchoTool()]
    model: str = "mock"

# Event listener
def print_event(event):
    # Emoji mapping for visual clarity
    emojis = {
        EventType.ORCHESTRA_START: "🎬",
        EventType.ORCHESTRA_END: "🏁",
        EventType.TASK_GENERATION_START: "🧠",
        EventType.TASK_GENERATION_END: "📋",
        EventType.TASK_START: "▶️",
        EventType.TASK_COMPLETE: "✅",
        EventType.TASK_ERROR: "❌",
        EventType.AGENT_START: "👤",
        EventType.AGENT_END: "🏁",
        EventType.TOOL_SELECTION: "🔨",
        EventType.TOOL_START: "⚙️",
        EventType.TOOL_END: "🆗",
        EventType.TOOL_ERROR: "💥",
        EventType.LOG: "📝"
    }
    
    emoji = emojis.get(event.type, "🔔")
    print(f"\n{emoji} [{event.type.name}] Source: {event.source}")
    try:
        print(f"   Data: {json.dumps(event.data, default=str, indent=2)}")
    except:
        print(f"   Data: {event.data}")

# Mock LLM response for agent execution
def mock_agent_invoke(*args, **kwargs):
    return {
        "tool_execution": {
            "tool_name": "echo",
            "tool_args": {"message": "Hello World"}
        },
        "reasoning": "The user wants me to say Hello World, so I will use the echo tool."
    }

def main():
    print("🧪 Testing Event Bus Integration...")
    
    # 1. Subscribe
    events.subscribe(print_event)

    # 2. Setup
    agent = EchoAgent()
    
    # 3. Create a manual task list
    task_list = TaskList(steps=[
        Task(
            step_number=1,
            task="Say Hello World",
            agent="echo_agent",
            expected_output="Echo: Hello World",
            is_async=False
        )
    ])

    # 4. Mock LLM
    with patch('orchestra.core.agent.model_invoke', side_effect=mock_agent_invoke):
        with patch('orchestra.core.task.model_invoke', return_value={"content": "Final Answer: Echo: Hello World"}):
            print("\n🚀 Starting Orchestra Run with Mock LLM...")
            run("Say Hello World", [agent], task_list=task_list)

if __name__ == "__main__":
    main()

