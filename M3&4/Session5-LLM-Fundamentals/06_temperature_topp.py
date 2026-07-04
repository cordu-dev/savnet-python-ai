"""
Step 06 — Temperature and top-p (the randomness dials)
======================================================

Two settings control how "adventurous" the model is when picking the next token:

    TEMPERATURE (0 to ~2):
        Low  (0.0)  -> pick the single most likely token. Focused, repeatable.
        High (1.0+) -> spread the odds around. Creative, varied, less reliable.

    TOP_P (0 to 1) — "nucleus sampling":
        Only consider the smallest set of tokens whose probabilities add up to p.
        top_p=1.0 = consider everything; top_p=0.3 = only the very likeliest few.

Rule of thumb:
    - Tune ONE of them, not both.
    - Extraction, SQL, classification, anything a program parses  -> temperature 0.
    - Brainstorming, drafting, rephrasing                          -> higher temp.

Why builders care:
    "Determinism" (same input -> same output) makes systems testable and
    debuggable. In production you usually want LOW temperature for that reason.

Run it:
    python 06_temperature_topp.py
"""

import llm_utils as llm

prompt = "Give one short idea to reduce foaming-station scrap."


def run_three_times(temperature):
    """Ask the same prompt 3x at a given temperature and print the replies."""
    model = llm.get_llm(temperature=temperature)
    print(f"\n=== temperature = {temperature} ===")
    for i in range(1, 4):
        reply = model.invoke(prompt).content.strip().replace("\n", " ")
        print(f"  {i}. {reply}")


# --- Low temperature: focused and repeatable -----------------------------
# You'll usually see the same (or nearly identical) idea all three times.
run_three_times(0.0)

# --- High temperature: creative and varied -------------------------------
# Expect three different ideas — great for brainstorming, risky for pipelines.
run_three_times(1.0)

# --- top_p in action ------------------------------------------------------
# Here we keep temperature moderate but restrict top_p to the likeliest tokens,
# which reins the variety back in.
model_narrow = llm.get_llm(temperature=1.0, top_p=0.2)
print("\n=== temperature = 1.0 but top_p = 0.2 (narrowed) ===")
for i in range(1, 4):
    print(f"  {i}.", model_narrow.invoke(prompt).content.strip().replace("\n", " "))

print(
    "\nTakeaway: for anything your CODE has to rely on, use temperature 0.\n"
    "Save the high settings for when you actually want variety."
)

# =========================================================================
# YOUR CHALLENGE (10 min)
# -------------------------------------------------------------------------
# 1. Which setting produced the most REPEATABLE answers? Why does that help
#    when you're writing automated tests for an agent?
# 2. Try temperature=1.8. Does quality drop? Where's the sweet spot for
#    brainstorming vs nonsense?
# 3. For each of these tasks, pick a temperature and justify it in one line:
#    (a) extracting a defect record, (b) writing a friendly report intro,
#    (c) generating SQL from a question.
# =========================================================================
