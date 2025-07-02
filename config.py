import os

from dotenv import load_dotenv

load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")
OPENAI_MODEL = os.getenv("OPENAI_MODEL")
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL")
QWEN_MODEL = os.getenv("QWEN_MODEL")

TEMPERATURE = os.getenv("TEMPERATURE")
