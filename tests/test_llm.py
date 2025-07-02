from llm.base import model_invoke
from llm.ollama_llm import ollama_invoke


def test_ollama_basic_completion():
    # Arrange
    system_message = "You are a helpful assistant"
    user_message = "Answer only with 'hello world!'"

    # Act
    result = ollama_invoke(system_message, user_message, payload=None)

    # Assert

    assert isinstance(result, str)
    assert len(result) > 0
    assert "hello world!" in result.lower()


def test_ollama_function_calling():
    # Arrange
    system_message = "You are a helpful assistant"
    user_message = "What's the weather in New York?"
    payload = {
        "name": "get_weather",
        "description": "Get the weather for a location",
        "parameters": {
            "type": "object",
            "properties": {"location": {"type": "string"}},
            "required": ["location"],
        },
    }

    # Act
    result = ollama_invoke(system_message, user_message, payload=payload)

    # Assert
    assert isinstance(result, dict)
    assert "location" in result
    assert result["location"].lower() == "new york"


def test_model_invoke():
    # Arrange
    system_message = "You are a helpful assistant"
    user_message = "Say 'hello world'"
    model = "ollama"

    # Act
    result = model_invoke(system_message, user_message, payload=None, model=model)

    # Assert
    assert isinstance(result, str)
    assert len(result) > 0
    assert "hello world" in result.lower()
