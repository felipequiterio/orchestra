import os
import sys

import ollama

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import DEEPSEEK_MODEL


def _get_tool_call(response: dict) -> dict:
    """Extract the first tool call and format it like `ToolAgent.execute()` expects."""

    tool_call = response["message"]["tool_calls"][0]
    function = tool_call["function"]

    tool_name = function.get("name")
    arguments = function.get("arguments", {})

    reasoning = response["message"].get("content", "") or "Automatically selected tool via model call."

    return {
        "tool_execution": {
            "tool_name": tool_name,
            "tool_args": arguments,
        },
        "reasoning": reasoning,
    }


def deepseek_invoke(system_message: str, user_message: str, payload: dict) -> dict:
    tools = None
    if payload:
        tools = [{"type": "function", "function": payload}]

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    response = ollama.chat(model=DEEPSEEK_MODEL, messages=messages, tools=tools)

    if payload:
        return _get_tool_call(response)

    return response["message"]["content"]
