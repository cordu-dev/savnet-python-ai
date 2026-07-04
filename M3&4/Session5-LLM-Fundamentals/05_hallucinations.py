"""
Step 05 — Hallucinations (confident nonsense)
=============================================

A hallucination is when the model states something FALSE with total confidence.
Remember step 01: it predicts plausible text. "Plausible" and "true" are not
the same thing — so it will happily invent part numbers, specs, and citations.

Why it happens:
    - It's optimised to produce likely-sounding text, not to admit ignorance.
    - It has no built-in "I don't actually know" signal unless you ask for one.
    - Vague or leading questions invite it to make things up.

Three practical defences you'll use all course:
    1. GROUND it — give it the facts in the prompt and tell it to use ONLY those.
    2. Give it an OUT — explicitly allow "I don't know" so it stops guessing.
    3. VERIFY — check the answer against a source (tools/DB) before trusting it.

Run it:
    python 05_hallucinations.py
"""

import llm_utils as llm

model = llm.get_llm(temperature=0.7)

# --- 1. Invite a hallucination -------------------------------------------
# This asks about a made-up product. The honest answer is "no idea", but a
# naive model often invents confident specs anyway.
leading = "What is the exact foam injection pressure for the ZF-9000X ProGrip wheel?"
print("=== Unguarded prompt (invites invention) ===")
print("Q:", leading)
print("A:", model.invoke(leading).content.strip())

# --- 2. Defence #2: give it permission to say 'I don't know' -------------
guarded = (
    "Answer only if you are certain. If you don't know, reply exactly "
    "'I don't have that information.'\n\n"
    "What is the exact foam injection pressure for the ZF-9000X ProGrip wheel?"
)
print("\n=== Same question, but we allow 'I don't know' ===")
print("A:", model.invoke(guarded).content.strip())

# --- 3. Defence #1: grounding in provided facts --------------------------
# We hand the model the ONLY facts it's allowed to use. This is the single most
# effective anti-hallucination technique, and it's how our SQL/data agents will
# work later: the answer must come from real retrieved data, not memory.
facts = "FACTS:\n- PT55 target foam volume: 8.0 ml (+/- 0.5 ml)\n- Molding temp: 180-220 C"
grounded = (
    f"{facts}\n\n"
    "Using ONLY the facts above, answer. If the facts don't cover it, say "
    "'Not in the provided data.'\n\n"
    "Question: What is the target foam volume for a PT55 wheel?"
)
print("\n=== Grounded in provided facts ===")
print("A:", model.invoke(grounded).content.strip())

grounded_miss = grounded.replace(
    "What is the target foam volume for a PT55 wheel?",
    "What is the laser power spec?",
)
print("\n=== Grounded, but the answer ISN'T in the facts ===")
print("A:", model.invoke(grounded_miss).content.strip())

print(
    "\nTakeaway: don't trust a confident tone. Ground the model in real data, "
    "give it an escape hatch, and verify anything that matters."
)

# =========================================================================
# YOUR CHALLENGE (15 min)
# -------------------------------------------------------------------------
# 1. Ask for "three research papers about steering-wheel scrap rates" with
#    authors and years. Try to verify them. How many are real?
# 2. Take a question the unguarded model got wrong and fix it using grounding.
#    Write down which defence worked best.
# 3. Curriculum homework: find 3 manufacturing questions where the model is
#    confidently wrong, and note how you'd CATCH each one in production.
# =========================================================================
