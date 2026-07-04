"""
Step 00 — Does my setup work?
=============================

Goal:
    Prove three things before you learn anything else:
        1. Your packages are installed.
        2. Your Gemini API key is loaded from .env.
        3. You can actually get a reply from the model.

If this script prints a friendly greeting from Gemini, you're ready. If it
errors, read the message — it tells you exactly what to fix.

Run it:
    python 00_setup_check.py

Prerequisites:
    - `pip install -r ../../requirements.txt` (with your .venv active)
    - A .env file with GOOGLE_API_KEY set (see README + .env.example)
"""

import llm_utils as llm

# --- 1. Is the key there? ------------------------------------------------
# check_key() raises a clear, step-by-step error if the key is missing, so we
# don't waste an API call only to get a confusing "unauthorized" later.
llm.check_key()
print("Step 1/3: API key found.")

# --- 2. Can we build the model object? -----------------------------------
# temperature=0 makes the reply as repeatable as possible — good for a test.
model = llm.get_llm(temperature=0)
print("Step 2/3: Model object created.")

# --- 3. Can we get a real reply? -----------------------------------------
# .invoke() sends a single message and waits for the full answer. The result
# is an AIMessage object; its text lives in the `.content` attribute.
prompt = "In one short sentence, greet a class learning to build AI agents."
response = model.invoke(prompt)

print("Step 3/3: Got a reply from Gemini:\n")
print("   ", response.content)

print("\nAll good — move on to 01_what_llm_does.py")

# =========================================================================
# YOUR CHALLENGE (5 min)
# -------------------------------------------------------------------------
# 1. Change the prompt to ask Gemini for a fun fact about steering wheels.
# 2. Print `response.response_metadata` — can you spot the token counts?
# 3. Run the script twice with temperature=0. Is the answer identical? Now
#    try temperature=1 twice. What changed? (We'll dig into this in step 06.)
# =========================================================================
