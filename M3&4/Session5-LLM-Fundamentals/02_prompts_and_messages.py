"""
Step 02 — Prompts, system instructions, and message history
===========================================================

So far we sent one plain string. Real chat apps send a LIST of messages, each
with a ROLE. Getting roles right is 80% of "prompt engineering".

The three roles you'll use constantly:
    - SystemMessage : the standing instructions / persona ("You are a...").
                      Set once; it shapes every reply. The model trusts it most.
    - HumanMessage  : what the user says.
    - AIMessage     : what the model said earlier (the conversation history).

Why history matters:
    The model has NO memory between calls. It only knows what you send THIS
    time. To have a "conversation", you resend the previous messages each turn.
    That growing list must fit inside the model's CONTEXT WINDOW — the maximum
    number of tokens it can read at once (think: its short-term attention span).

Run it:
    python 02_prompts_and_messages.py
"""

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

import llm_utils as llm

model = llm.get_llm(temperature=0.3)

# --- 1. A system message sets the behaviour ------------------------------
# Notice we never repeat "be concise" — the system message handles it for the
# whole conversation.
system = SystemMessage(
    content=(
        "You are a manufacturing quality assistant. "
        "Answer in one short, plain-English sentence. No jargon."
    )
)

# --- 2. First turn -------------------------------------------------------
messages = [system, HumanMessage(content="What is 'scrap rate'?")]
first_reply = model.invoke(messages)
print("Q1: What is 'scrap rate'?")
print("A1:", first_reply.content.strip(), "\n")

# --- 3. Second turn — we must resend the history -------------------------
# We append the model's own answer (as an AIMessage) and the new question.
# The word "it" only makes sense because the model can see the earlier turn.
messages.append(AIMessage(content=first_reply.content))
messages.append(HumanMessage(content="Is a high one good or bad?"))

second_reply = model.invoke(messages)
print("Q2: Is a high one good or bad?   (note: 'it' relies on memory of Q1)")
print("A2:", second_reply.content.strip())

# --- 4. Proof that memory is manual --------------------------------------
# Ask the SAME follow-up with NO history and watch it lose the thread.
print("\n--- Same follow-up, but WITHOUT history ---")
no_history = model.invoke([system, HumanMessage(content="Is a high one good or bad?")])
print("A:", no_history.content.strip())
print("\nWithout the earlier turn, the model doesn't know what 'one' means.")

# =========================================================================
# YOUR CHALLENGE (10 min)
# -------------------------------------------------------------------------
# 1. Rewrite the SystemMessage to make the assistant answer like a strict
#    auditor who always mentions a tolerance range. Re-run — how do replies
#    change without touching the questions?
# 2. Add a THIRD turn ("How would I reduce it?") and keep the history correct.
# 3. Roughly how many tokens is your full message list now? (Use
#    llm.estimate_tokens on the combined text.) Why does this number matter
#    for cost and for the context window?
# =========================================================================
