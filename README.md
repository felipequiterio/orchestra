# Orchestra 🎻

**An AI Agent Orchestration Framework**

[![Tests](https://github.com/yourusername/orchestra/actions/workflows/tests.yml/badge.svg)](https://github.com/yourusername/orchestra/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Orchestra is a framework for building and coordinating AI agents with tool usage capabilities. Designed for local LLM workflows with native Ollama support.

```python
from orchestra import run
from core.agent import ToolAgent
from core.tools import Tool

# Define a specialized agent
class MathAgent(ToolAgent):
    name = "Math Expert"
    description = "Handles mathematical calculations and operations"
    tools = [Calculator()]
    model = "ollama"

# Create a tool
class Calculator(Tool):
    def run(self, expression: str) -> float:
        return eval(expression)
    
    def get_schema(self):
        return super().get_schema()  # Auto-generated from run() params

# Complete task orchestration in one call
response = run(
    "What's the weather in Tokyo and calculate 15% of 84590?",
    agent_list=[MathAgent()]
)
```

## Key Features

- 🧩 **Pluggable Agents** - Create specialized agents with custom tools
- 🛠️ **Automatic Tool Schema** - Parameter validation from code signatures
- 🔄 **Conversation History** - Full context tracking across executions
- 🤖 **Multi-LLM Support** - Switch between Ollama, DeepSeek, and more
- ⚡ **UV Powered** - Lightning-fast dependency management
- 🔄 **Async Task Support** - Run tasks in parallel when possible
- 🎯 **Smart Task Routing** - Automatic task decomposition and agent assignment

## Quick Start

1. **Install with UV**:

```bash
git clone https://github.com/yourusername/orchestra.git
cd orchestra
```

2. **Configure Environment**:

```bash
uv venv
```

3. **Install Dependencies**:

```bash
uv sync
```

4. **Run Tests**:

```bash
uv run pytest tests/ -v
```

## Core Concepts

### Agents

Define specialized actors with tools:

```python
from core.agent import ToolAgent

class MathAgent(ToolAgent):
    name = "Math Expert"
    description = "Handles mathematical calculations and operations"
    tools = [Calculator()]
    model = "ollama"
```

### Tools

Create reusable capabilities:

```python
from core.tools import Tool

class Calculator(Tool):
    def run(self, expression: str) -> float:
        return eval(expression)
    
    def get_schema(self):
        return super().get_schema()  # Auto-generated from run() params
```

### Task Management

Orchestra automatically decomposes complex queries into tasks and routes them to appropriate agents:

```python
from core.task import TaskList, Task

# Manual task definition (optional)
tasks = TaskList(steps=[
    Task(
        step_number=1,
        task="Calculate 15% of 84590",
        agent="math_agent",
        expected_output="The result of the calculation",
        is_async=False
    )
])

# Automatic task generation (default)
response = run("Complex math query", agent_list=[MathAgent()])
```

## Project Structure

```
orchestra/
├── core/            # Framework internals
│   ├── agent.py     # Base agents and agent management
│   ├── handler.py   # Request/response handling
│   ├── task.py      # Task generation and routing
│   └── tools.py     # Tool infrastructure
├── llm/             # LLM integrations
├── utils/           # Utility functions
├── examples/        # Example implementations
├── tests/           # Pytest tests
└── orchestra.py     # Main interface
```

## License

MIT © 2024 Your Name
