from orchestra.llm.deepseek_llm import deepseek_invoke
from orchestra.llm.ollama_llm import ollama_invoke


def model_invoke(
    system_message: str,
    user_message: str,
    payload: dict = None,
    model: str = "ollama",
) -> dict:
    if model == "ollama":
        return ollama_invoke(system_message, user_message, payload)
    elif model == "deepseek":
        return deepseek_invoke(system_message, user_message, payload)
    else:
        raise ValueError(
            f"Invalid model: {model}. Models avaiable: ollama, deepseek, openai"
        )
