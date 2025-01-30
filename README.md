# Orchestra Framework (Work in Progress)

> ⚠️ **Note**: Orchestra is currently under active development and in its early stages. APIs and functionality may change significantly. This is a proof of concept and not yet ready for production use.

Orchestra is a flexible framework for building and orchestrating AI agents. It provides a structured way to create, manage, and coordinate multiple AI agents to handle complex tasks through natural language.

## Current Development Status

The framework is being actively developed with the following components in progress:

✅ Basic agent structure and registration
✅ Task generation using LLMs
✅ Simple task routing
🚧 Agent tool decorator (In Progress)
🚧 LLM provider integrations (In Progress)
❌ Async execution support (Planned)
❌ Production-ready error handling (Planned)
❌ Comprehensive test coverage (Planned)

## Overview

Orchestra aims to allow you to:

- Create specialized AI agents with specific capabilities
- Route user queries to appropriate agents automatically
- Handle multi-step tasks with dependencies
- Execute tasks both synchronously and asynchronously
- Integrate with different LLM providers (Ollama, DeepSeek, etc.)

## Installation

> ⚠️ **Note**: As this is a work in progress, installation from PyPI is not yet available.

1. Clone the repository:

```bash
git clone https://github.com/yourusername/orchestra.git
cd orchestra
```

2. Install the dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:

```bash
OLLAMA_MODEL=mistral
DEEPSEEK_MODEL=your_model
TEMPERATURE=0.7
```

## Core Concepts

### Agents

Agents are specialized components that handle specific types of tasks. Each agent inherits from the `ToolAgent` base class:

```python
from orchestra.core.agent import ToolAgent, AgentTask
class WeatherAgent(ToolAgent):
    name: str = "Weather Agent"
    description: str = (
        "You are a weather manager responsible for fetching weather information"
    )

    @agent.tool
    def fetch_weather(self, city: str) -> Dict:
        temperature = 20
        city = "New York City"
        return {"status": "success", "message": f"Weather in {city} is {temperature} degrees"}
```

### Tasks

Tasks represent units of work to be performed by agents. They are automatically generated from user queries and contain:

- Step number
- Task description
- Target agent
- Expected output
- Async flag

```python
from orchestra.core.task import Task
task = Task(
    step_number=1,
    task="Fetch weather for New York",
    agent="weather_agent",
    expected_output="Current weather conditions",
    is_async=False
)
```

### Agent Handler

The `AgentHandler` class manages agent registration and retrieval:

```python
from orchestra.core.handler import AgentHandler
from examples.weather_agent import WeatherAgent
from examples.todo_agent import TodoAgent

handler = AgentHandler()

handler.register(WeatherAgent())
handler.register(TodoAgent())

agents = handler.list_agents()
```

## Usage Example

Here's a complete example of using Orchestra:

```python
from orchestra.core.handler import AgentHandler
from orchestra.core.task import Task
from examples.agents import WeatherAgent, TodoAgent

# Initialize and register agents
handler = AgentHandler()
handler.register(WeatherAgent())
handler.register(TodoAgent())

# Process a user query
query = "Add 'Buy groceries' to my todo list and check the weather in New York"

# Generate tasks from the query
task_list = Task.generate(query, handler.list_agents())

# Execute tasks
results = Task.route(task_list, handler.list_agents())

# Results will contain responses from both agents
print(results)
```

This example demonstrates how to create agents, generate tasks from user queries, and execute them in a coordinated manner.

## Project Structure

```
orchestra/
├── core/
│ ├── agent.py # Base agent classes
│ ├── handler.py # Agent management
│ └── task.py # Task generation/routing
├── llm/
│ ├── base.py # LLM interface
│ ├── ollama.py # Ollama integration
│ └── deepseek.py # DeepSeek integration
├── utils/
│ ├── logger.py # Logging utilities
│ └── validation.py # Input validation
├── examples/ # Example agents
└── tests/ # Test suite
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Development Status

Orchestra is currently in active development. Key items on the roadmap:

- [ ] Agent tool decorator implementation
- [ ] Mock agent implementations for test purposes
- [ ] Fix Task.generate() function
- [ ] Async execution support
- [ ] Additional LLM provider integrations

## License

This project is licensed under the MIT License - see the LICENSE file for details.
