"""
Session 5 — Shared LLM helpers
==============================

This is the ONE place where we set up the connection to the LLM. Every numbered
script imports from here so we don't repeat the same boilerplate nine times.

Think of it like `data_utils.py` from Session 4, but instead of loading Parquet
files, it hands you a ready-to-use *language model object*.

Why a separate file?
    - Setup logic (API key, model choice) lives in one spot.
    - If Google renames a model or you switch providers, you edit ONE file.
    - The teaching scripts stay short and focused on a single idea.

What is an "LLM object"?
    `ChatGoogleGenerativeAI` is LangChain's wrapper around Google's Gemini API.
    You give it messages, it returns the model's reply. LangChain gives every
    provider (Gemini, OpenAI, Claude, Groq...) the SAME interface, so the code
    you learn here transfers to any of them later.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# 1. Load the API key from the .env file
# ---------------------------------------------------------------------------
# load_dotenv() reads the ".env" file sitting next to this module and copies
# its values into environment variables. We point it at an explicit path so it
# works no matter which folder you launch Python from.
_ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(_ENV_PATH)

# The default free model. "flash" is fast and cheap; great for learning.
# (Gemini also has "gemini-2.5-flash-lite" with a higher daily request cap,
#  and "gemini-2.5-pro" for harder reasoning. Verify names at ai.google.dev.)
DEFAULT_MODEL = "gemini-2.5-flash"


def check_key() -> str:
    """
    Return the Gemini API key, or raise a friendly error explaining how to fix
    a missing/blank key. Call this at the top of any script that talks to the LLM.
    """
    key = os.getenv("GOOGLE_API_KEY", "").strip()
    if not key or key == "paste-your-key-here":
        raise RuntimeError(
            "\n\n"
            "No Gemini API key found.\n"
            "Fix it in three steps:\n"
            "  1. Get a free key: https://aistudio.google.com/apikey\n"
            "  2. Copy .env.example to .env  ->  cp .env.example .env\n"
            "  3. Paste your key after GOOGLE_API_KEY= and save.\n"
        )
    return key


def get_llm(temperature: float = 0.7, model: str = DEFAULT_MODEL, **kwargs):
    """
    Build and return a Gemini chat model.

    Parameters
    ----------
    temperature : float
        Creativity/randomness dial (0 = focused & repeatable, 1+ = wilder).
        We explore this in 06_temperature_topp.py.
    model : str
        Which Gemini model to use. Defaults to a fast, cheap one.
    **kwargs :
        Anything else LangChain's ChatGoogleGenerativeAI accepts
        (e.g. top_p, max_output_tokens).
    """
    check_key()
    # Imported here (not at top) so scripts that only need count_tokens() can
    # run even before `pip install langchain-google-genai` finishes.
    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(model=model, temperature=temperature, **kwargs)


# ---------------------------------------------------------------------------
# 2. Rough token + cost helpers (used in 07_token_costs.py)
# ---------------------------------------------------------------------------
# A "token" is a chunk of text the model reads/writes — often ~4 characters of
# English, or roughly 3/4 of a word. This is only an ESTIMATE. For exact counts
# you'd use the provider's tokenizer, but the 4-chars rule is close enough to
# build good cost intuition.
CHARS_PER_TOKEN = 4


def estimate_tokens(text: str) -> int:
    """Very rough token count: about 1 token per 4 characters."""
    return max(1, len(text) // CHARS_PER_TOKEN)


def estimate_cost(input_tokens: int, output_tokens: int,
                  input_per_million: float = 0.10,
                  output_per_million: float = 0.40) -> float:
    """
    Estimate US-dollar cost of one call.

    Prices are PER MILLION tokens and change often — the defaults are
    illustrative Gemini-Flash-style numbers. Always check current pricing at
    https://ai.google.dev/pricing before quoting real costs.
    """
    return (input_tokens / 1_000_000) * input_per_million + \
           (output_tokens / 1_000_000) * output_per_million


if __name__ == "__main__":
    # Quick self-test you can run: `python llm_utils.py`
    print("Token estimate for 'Hello factory floor':",
          estimate_tokens("Hello factory floor"))
    print("Cost of 1000 in / 500 out tokens: $",
          round(estimate_cost(1000, 500), 6))
    try:
        check_key()
        print("API key found ✓  — you're ready to run 00_setup_check.py")
    except RuntimeError as err:
        print(err)
