"""
Session 7 — Shared LLM helpers for Mistral
==========================================

This module centralizes the connection to the Mistral AI model,
specifically Codestral for SQL/routing and Mistral-Large if needed.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load the API key from the local .env file
_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(_ENV_PATH)

DEFAULT_MODEL = "codestral-latest"


def check_key() -> str:
    """
    Return the Mistral API key, or raise a friendly error explaining how to fix
    a missing/blank key.
    """
    key = os.getenv("MISTRAL_API_KEY", "").strip()
    if not key or key == "paste-your-key-here":
        raise RuntimeError(
            "\n\n"
            "No Mistral API key found.\n"
            "Fix it in three steps:\n"
            "  1. Get a free key: https://console.mistral.ai/\n"
            "  2. Copy .env.example to .env  ->  cp .env.example .env\n"
            "  3. Paste your key after MISTRAL_API_KEY= and save.\n"
        )
    return key


def get_llm(temperature: float = 0.0, model: str = DEFAULT_MODEL, **kwargs):
    """
    Build and return a Mistral chat model.
    """
    check_key()
    
    from langchain_mistralai import ChatMistralAI

    return ChatMistralAI(
        model=model,
        temperature=temperature,
        api_key=os.getenv("MISTRAL_API_KEY"),
        **kwargs
    )


if __name__ == "__main__":
    try:
        check_key()
        print("API key found ✓  — you're ready to run Session 7 scripts.")
    except RuntimeError as err:
        print(err)
