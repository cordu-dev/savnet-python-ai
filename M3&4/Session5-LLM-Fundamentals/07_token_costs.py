"""
Step 07 — Token costs (build cheap habits early)
================================================

You pay LLMs by the TOKEN, not by the question. Two kinds:
    - INPUT tokens  : everything you SEND (system message + history + question).
    - OUTPUT tokens : everything the model WRITES back.

A token is ~4 characters of English (~3/4 of a word). "Steering wheel scrap
rate" is roughly 6-7 tokens.

Why this bites you:
    - Resending long chat history every turn (step 02) means input tokens grow
      every message. A 20-turn chat can cost far more than you'd guess.
    - Verbose system prompts and "just in case" context add up across thousands
      of calls.

Two numbers to always know:
    1. How big is my prompt? (estimate before sending)
    2. What did the call actually use? (read it back from the response)

Run it:
    python 07_token_costs.py
"""

import llm_utils as llm

model = llm.get_llm(temperature=0)

short_prompt = "List 3 causes of molding scrap."
long_prompt = (
    "You are a senior manufacturing engineer with 20 years of experience across "
    "molding, foaming, conductor, laser, and tapitat stations. Consider all "
    "historical shift data, material batches, operator notes, and maintenance "
    "logs. Think step by step and be extremely thorough. " + short_prompt
)

# --- 1. Estimate BEFORE you send -----------------------------------------
# Cheap habit: sanity-check prompt size before firing off thousands of calls.
print("Rough input-token estimates (before sending):")
print("  short prompt:", llm.estimate_tokens(short_prompt), "tokens")
print("  long  prompt:", llm.estimate_tokens(long_prompt), "tokens")
print("  -> the padded prompt costs ~"
      f"{llm.estimate_tokens(long_prompt) // llm.estimate_tokens(short_prompt)}x"
      " more INPUT tokens, for a similar answer.\n")

# --- 2. Read the ACTUAL usage after the call -----------------------------
# Providers report exact token counts. LangChain exposes them on the response.
# This is the source of truth — our estimate is just a quick guess.
reply = model.invoke(short_prompt)
usage = reply.usage_metadata  # dict: input_tokens, output_tokens, total_tokens
print("Actual usage reported by Gemini:")
print(" ", usage)

if usage:
    cost = llm.estimate_cost(usage["input_tokens"], usage["output_tokens"])
    print(f"\nIllustrative cost of this one call: ${cost:.6f}")
    calls_for_a_dollar = int(1 / cost) if cost else 0
    print(f"That's ~{calls_for_a_dollar:,} calls like this per $1 (prices vary!).")

print(
    "\nTakeaway: trim system prompts, don't resend history you don't need, and\n"
    "cap output length. Small savings x thousands of calls = real money."
)

# =========================================================================
# YOUR CHALLENGE (10 min)
# -------------------------------------------------------------------------
# 1. Add max_output_tokens=50 via llm.get_llm(..., max_output_tokens=50). How
#    do the output tokens and cost change?
# 2. Simulate a 10-turn chat by building a message list that keeps growing.
#    Estimate the input tokens at turn 1 vs turn 10. What does this tell you
#    about long conversations?
# 3. Curriculum homework: call the API with 10 manufacturing questions, parse
#    the structured JSON (reuse step 03), and total the tokens/cost. What broke?
# =========================================================================
