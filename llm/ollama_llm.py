import os
import sys

import ollama

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from config import OLLAMA_MODEL


def get_arguments(response: dict) -> dict:
    """Extract tool arguments from Ollama response with proper error handling"""
    try:
        # Check if response has the expected structure
        if "message" in response and "tool_calls" in response["message"]:
            tool_calls = response["message"]["tool_calls"]
            if tool_calls and len(tool_calls) > 0:
                return tool_calls[0]["function"]["arguments"]
        
        # If tool_calls structure is missing, try to parse the content as JSON
        if "message" in response and "content" in response["message"]:
            import json
            content = response["message"]["content"]
            if content:
                try:
                    # Try to parse the content as JSON
                    return json.loads(content)
                except json.JSONDecodeError:
                    # If parsing fails, wrap the content as a generic response
                    return {"response": content}
        
        # Last fallback - return the entire response
        return response
    except (KeyError, IndexError, TypeError) as e:
        # Fallback for any structural issues
        return {"error": f"Failed to parse response: {str(e)}", "raw_response": response}


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
