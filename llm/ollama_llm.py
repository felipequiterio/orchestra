import ollama
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import OLLAMA_MODEL, QWEN_MODEL

def get_arguments(response: dict) -> dict:
    return response["message"]["tool_calls"][0]["function"]["arguments"]

def ollama_invoke(system_message: str, user_message: str, payload: dict) -> dict:
    tools = None
    if payload:
        tools = [{"type": "function", "function": payload}]

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_message},
    ]

    response = ollama.chat(model=OLLAMA_MODEL, messages=messages, tools=tools)

    if payload:
        response = get_arguments(response)
        return response

    return response["message"]["content"]