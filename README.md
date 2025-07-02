# Orchestra 🎻

**An AI Agent Orchestration Framework**

Orchestra is a powerful framework for building and coordinating AI agents with seamless tool integration. Designed for modern AI workflows, it provides native support for local LLMs through Ollama while maintaining flexibility for cloud-based models. Whether you're building simple automation scripts or complex multi-agent systems, Orchestra simplifies the orchestration process with its intuitive API and robust tool management system.

## Quick Start

```bash
pip install orchestra
```

## Example



```python
from orchestra import run
from core.agent import ToolAgent
from core.tools import Tool

# Define a specialized agent
class MathAgent(ToolAgent):
    name = "Math Expert"
    description = "Handles mathematical calculations and operations"
    backstory = "A mathematical expert capable of complex calculations"
    system_prompt = "You are a math expert. Use the calculator tool to solve mathematical problems."
    input_schema = {"type": "object", "properties": {"expression": {"type": "string"}}}
    output_schema = {"type": "object", "properties": {"result": {"type": "number"}}}
    tools = [Calculator()]
    model = "ollama"

# Create a tool
class Calculator(Tool):
    name = "calculator"
    description = "Performs mathematical calculations"
    
    def run(self, expression: str) -> float:
        """Calculate the result of a mathematical expression"""
        return eval(expression)

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

3. **Set up environment variables**:

Create a `.env` file with your model configurations:
```bash
OLLAMA_MODEL=llama3.2
DEEPSEEK_MODEL=deepseek-coder
OPENAI_MODEL=gpt-4
QWEN_MODEL=qwen2.5
TEMPERATURE=0.7
```

4. **Install Dependencies**:

```bash
uv sync
```

5. **Run Tests**:

```bash
uv run pytest tests/ -v
```

## Core Concepts

### Agents

Define specialized actors with tools by inheriting from `ToolAgent`:

```python
from core.agent import ToolAgent

class MathAgent(ToolAgent):
    name = "Math Expert"
    description = "Handles mathematical calculations and operations"
    backstory = "A mathematical expert capable of complex calculations"
    system_prompt = "You are a math expert. Use the calculator tool to solve mathematical problems."
    input_schema = {"type": "object", "properties": {"expression": {"type": "string"}}}
    output_schema = {"type": "object", "properties": {"result": {"type": "number"}}}
    tools = [Calculator()]
    model = "ollama"
```

### Tools

Create reusable capabilities by inheriting from `Tool`:

```python
from core.tools import Tool

class Calculator(Tool):
    name = "calculator"
    description = "Performs mathematical calculations"
    
    def run(self, expression: str) -> float:
        """Calculate the result of a mathematical expression"""
        return eval(expression)
    
    # Schema is automatically generated from the run() method signature
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

### Agent Handler

Manage agent registration and retrieval:

```python
from core.handler import AgentHandler

handler = AgentHandler()
handler.register(MathAgent())
agent = handler.get_agent("Math Expert")
```

## Project Structure

```
orchestra/
├── core/            # Framework internals
│   ├── agent.py     # Base agents and agent management
│   ├── handler.py   # Agent registration and retrieval
│   ├── task.py      # Task generation and routing
│   └── tools.py     # Tool infrastructure
├── llm/             # LLM integrations
│   ├── base.py      # Model invocation interface
│   ├── ollama_llm.py # Ollama integration
│   └── deepseek_llm.py # DeepSeek integration
├── utils/           # Utility functions
│   └── logger.py    # Custom logging setup
├── examples/        # Example implementations
├── tests/           # Pytest tests
├── config.py        # Environment configuration
└── orchestra.py     # Main interface
```

## Configuration

The framework uses environment variables for configuration. Create a `.env` file:

```bash
# Model configurations
OLLAMA_MODEL=llama3.2
DEEPSEEK_MODEL=deepseek-coder
OPENAI_MODEL=gpt-4
QWEN_MODEL=qwen2.5

# Generation settings
TEMPERATURE=0.7
```

## Dependencies

- **Python**: >=3.12
- **ollama**: >=0.4.7
- **pydantic**: >=2.10.6
- **python-dotenv**: >=1.0.1
- **colorama**: >=0.4.6

## License

MIT © 2024 Your Name
