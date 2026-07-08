"""
Step 00 — Does my Mistral setup work?
======================================

Goal:
    Prove three things before starting:
        1. Your packages are installed (including `langchain-mistralai`).
        2. Your Mistral API key is loaded from `.env`.
        3. You can get a successful reply from the Codestral model.

Run it:
    python 00_setup_check.py

Prerequisites:
    - Make sure your virtual environment is active.
    - Run: `pip install langchain-mistralai`
    - Create a `.env` file with your `MISTRAL_API_KEY` (see `.env.example`).
"""

import llm_utils as llm

# --- 1. Check API Key ----------------------------------------------------
try:
    llm.check_key()
    print("Step 1/3: Mistral API key found.")
except RuntimeError as err:
    print(err)
    exit(1)

# --- 2. Build Model Object -----------------------------------------------
# We use temperature=0 for SQL generation.
try:
    model = llm.get_llm(temperature=0)
    print("Step 2/3: Mistral model object created successfully.")
except Exception as err:
    print(f"Error creating model object: {err}")
    exit(1)

# --- 3. Get a Response ---------------------------------------------------
try:
    prompt = "In one short sentence, greet a class of manufacturing engineers learning to build AI SQL agents."
    print("Step 3/3: Sending prompt to Mistral Codestral...")
    response = model.invoke(prompt)
    print("\nReply from Codestral:\n")
    print("   ", response.content.strip())
    print("\nAll systems go! Ready to proceed to 01_schema_extractor.py")
except Exception as err:
    print(f"\nAPI Call Failed: {err}")
    print("Double check that your MISTRAL_API_KEY is active and correct.")

# =========================================================================
# YOUR CHALLENGE (5 min)
# -------------------------------------------------------------------------
# 1. Change the prompt to ask Mistral for a fun fact about DuckDB.
# 2. Print `response.response_metadata`. Do you see the token usage stats?
#    Look for `token_usage` or similar fields in the dictionary.
# 3. Mistral's Codestral model is highly specialized. Ask it to write a
#    quick Python function to calculate scrap rate: does it write clean code?
# =========================================================================
