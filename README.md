# Orchestra 🎻

> An ergonomic Python framework for **tool-augmented AI agents** and multi-step orchestration.

Orchestra lets you wire up specialised agents, equip them with arbitrary Python tools and hand the framework a natural-language query. It decomposes the request into a task list, routes every task to the right agent (sync or async), runs the tools and finally merges all partial results into a single, conversational answer.

It is the **missing glue** between your own Python code and whichever Large-Language-Models (LLMs) you run locally or in the cloud.

---

## ✨ Key Capabilities

* **Pluggable agents** – subclass `ToolAgent`, give it a `Tool` list and you are done.
* **Automatic tool schema** – the JSON schema for a tool is built straight from your `run()` signature and doc-string.
* **Smart task router** – an LLM decomposes the user query into ordered steps and assigns the best agent for each.
* **Async execution** – mark tasks as `is_async=true` to let Orchestra run them in parallel.
* **Model agnostic** – works with local [Ollama](https://ollama.ai/) models out of the box but can call OpenAI, DeepSeek, Qwen… anything you expose through `llm.base.model_invoke()`.
* **Batteries included** – shipping example agents for weather, todo management and calculations.

---

## 🛠 Installation

Orchestra is not on PyPI (yet). Clone the repo and install the dependencies with [uv](https://github.com/astral-sh/uv):

```bash
# 1. clone
$ git clone https://github.com/yourusername/orchestra.git && cd orchestra

# 2. create virtualenv
$ uv venv              # or: python -m venv .venv && source .venv/bin/activate

# 3. install deps
$ uv sync
```

Make sure an LLM is available. For example, with Ollama:

```bash
ollama run llama3
```

---

## ⚡ Quick Start

```python
from orchestra import run
from examples.example_usage import WeatherAgent, TodoAgent, CalculatorAgent

# Bundle the agents you want the router to pick from
agents = [WeatherAgent(), TodoAgent(), CalculatorAgent()]

query = "What's the weather in Tokyo and calculate 15% of 84590? Also add 'Buy groceries' to my todo list."

print(run(query, agents))
```

Output (truncated):

```
⚡ Task 1 (Step 1)
Status: ✅ SUCCESS
Tool: get_weather
Output: Weather in Tokyo, JP: 22°C, Sunny

⚡ Task 2 (Step 2)
Status: ✅ SUCCESS
Tool: calculate
Result: 12688.5

🔄 Task 3 (Step 3)
Status: ✅ SUCCESS
Tool: manage_todo
Output: Added 'Buy groceries' to todo list

Final answer:
Tokyo is currently sunny at 22 °C. 15 % of 84 590 is 12 688.5. And I've added "Buy groceries" to your todo list ✅
```

---

## 🧩 Building Blocks

### 1. Tools
Inherit from `core.tools.Tool` and implement `run()`. Parameters become part of the JSON schema automatically:

```python
from core.tools import Tool

class CalculatorTool(Tool):
    """Basic maths using python eval (do **not** use in production!)."""
    name = "calculate"
    description = "Perform mathematical calculations"

    def run(self, expression: str) -> float:
        """expression: any Python/NumPy compatible expression"""
        return eval(expression)
```

### 2. Agents
Wrap one or more tools and add personas by subclassing `core.agent.ToolAgent`:

```python
from core.agent import ToolAgent
from typing import Dict, Any, List

class CalculatorAgent(ToolAgent):
    name: str = "calculator_agent"
    description: str = "Specialised agent for mathematical calculations"
    backstory: str = "A mathematical computation expert that can perform various calculations accurately."
    system_prompt: str = "You are a mathematical computation expert. Always use the calculator tool to ensure accuracy."

    input_schema: Dict[str, Any] = {"type": "object", "properties": {"expression": {"type": "string"}}}
    output_schema: Dict[str, Any] = {"type": "object", "properties": {"result": {"type": "number"}}}

    tools: List[Tool] = [CalculatorTool()]
    model: str = "ollama"
```

### 3. Orchestration `run()`
Simply call `orchestra.run(query, agent_list)` – the framework takes care of everything else:

1. Generate/validate a `TaskList` out of the natural-language query.
2. Route each task to its designated agent.
3. Execute the selected tool with the provided arguments.
4. Merge the partial responses into a concise answer.

---

## ⚙️ Configuration

Set environment variables (or a `.env` file) to control the LLM backend and generation settings:

```bash
# .env
OLLAMA_MODEL=llama3
OPENAI_MODEL=gpt-4o
DEEPSEEK_MODEL=deepseek-coder
TEMPERATURE=0.7
```

---

## 🧪 Running Tests

```bash
uv run pytest -q
```

---

## 🗂 Project Layout

```
orchestra/
├── core/               # framework internals (agents, tasks, tools)
├── examples/           # runnable usage examples
├── llm/                # backend-specific model adapters
├── utils/              # logging and helpers
└── orchestra.py        # public API – the `run()` entry-point
```

---

## 📜 License

[MIT](LICENSE) © 2024 Your Name
