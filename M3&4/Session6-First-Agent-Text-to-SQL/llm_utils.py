"""
Session 6 — Shared LLM helpers for Mistral
==========================================

This is the ONE place where we set up the connection to the Mistral AI model.
Every numbered script imports from here so we don't repeat the same boilerplate.

Why Mistral AI?
    - Mistral provides an exceptional free tier with high rate limits for learning.
    - We use their specialized coding model, Codestral, which is fine-tuned
      specifically for code and SQL generation.

What is an "LLM object"?
    `ChatMistralAI` is LangChain's wrapper around Mistral's chat API.
    It provides the same unified interface as ChatGoogleGenerativeAI or ChatOpenAI.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load the API key from the .env file sitting next to this module
_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(_ENV_PATH)

# Default model: codestral-latest is Mistral's model optimized for code and SQL
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

    Parameters
    ----------
    temperature : float
        Creativity dial (0 = focused & repeatable, 1+ = wilder).
        For SQL generation, we ALWAYS use temperature=0 for max determinism.
    model : str
        Which Mistral model to use. Defaults to "codestral-latest".
    """
    check_key()
    
    # Import here so that scripts can run utility functions even if langchain-mistralai
    # is still installing.
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
        print("API key found ✓  — you're ready to run 00_setup_check.py")
    except RuntimeError as err:
        print(err)
