"""
Step 01 — What an LLM actually does
===================================

The single most important mental model in this whole course:

    An LLM is a NEXT-TOKEN PREDICTOR. It reads the text so far and guesses the
    most likely next chunk of text (a "token"), over and over. That's it.

    It is NOT looking things up in a database. It is NOT reasoning like a
    calculator. It is a very, very good "autocomplete" that has read most of
    the internet. Sometimes that confident autocomplete is wrong (step 05).

Analogy:
    Your phone keyboard suggests the next word as you type. An LLM is that same
    idea, scaled up billions of times and trained on far more text.

Why you care as a builder:
    - Because it PREDICTS text, the same prompt can give DIFFERENT answers.
    - Because it PREDICTS text, it will happily invent a confident-sounding
      answer even when it doesn't know. Knowing this prevents nasty surprises.

Run it:
    python 01_what_llm_does.py
"""

import llm_utils as llm

# We use a slightly creative temperature so the "same prompt, different answer"
# effect is easy to see. (More on temperature in step 06.)
model = llm.get_llm(temperature=0.9)

prompt = "Complete this sentence in 8 words or fewer: 'A steering wheel is'"

print("Prompt:", prompt)
print("\nAsking the SAME prompt three times...\n")

# --- Same input, different outputs ---------------------------------------
# If the LLM were a lookup table, all three answers would be identical. They
# usually aren't — proof that it is *sampling* likely continuations, not
# retrieving one true answer.
for i in range(1, 4):
    reply = model.invoke(prompt)
    print(f"  Attempt {i}: {reply.content.strip()}")

print(
    "\nSee how the wording changes? The model isn't 'remembering' one answer —\n"
    "it's predicting a plausible continuation each time. That is the core idea."
)

# =========================================================================
# YOUR CHALLENGE (10 min)
# -------------------------------------------------------------------------
# 1. Set temperature=0 and run again. Do the three answers become identical
#    (or nearly so)? Why would low temperature reduce the variation?
# 2. Ask it to "predict the next 3 words after: 'The scrap rate on line 4'".
#    Notice it happily continues text it has never actually seen.
# 3. In one sentence, write your own definition of what an LLM does. Keep it.
#    You'll refine it as the session goes on.
# =========================================================================
