"""
Step 08 — ReAct from scratch (the thinking loop behind agents)
==============================================================

Everything so far was ONE call. An AGENT loops: it thinks, acts, looks at the
result, and thinks again — until it can answer. The most famous pattern for
this is ReAct = REASoning + ACTing.

Each turn the model produces:
    Thought:      its reasoning about what to do next
    Action:       the name of a tool to use
    Action Input: the argument for that tool
...then WE run the tool and feed the result back as:
    Observation:  what the tool returned
The loop repeats. When the model is ready it writes:
    Final Answer: the response to the user

We build the loop BY HAND here (no framework) so you can SEE every step. Later
in the course, LangGraph will manage loops like this for you — but you'll know
exactly what's happening under the hood.

Context engineering angle:
    Notice what we put in the prompt each turn: the tools available, the format
    rules, and the growing Thought/Action/Observation transcript. Deciding what
    goes into that context — and what to leave out — is "context engineering".

We use GENERIC toy tools (a calculator and a fake search) to keep the focus on
the pattern, not on any dataset.

Run it:
    python 08_react_from_scratch.py
"""

import re

import llm_utils as llm


# --- 1. The toy tools -----------------------------------------------------
# Plain Python functions. Each takes a string and returns a string.
def calculator(expression: str) -> str:
    """Evaluate a simple math expression like '37 / 1250 * 100'."""
    # We only allow digits and basic math symbols — never eval() raw user text
    # in real code; this whitelist keeps the toy demo safe.
    if not re.fullmatch(r"[0-9+\-*/().\s]+", expression):
        return "Error: only numbers and + - * / ( ) are allowed."
    try:
        return str(round(eval(expression), 4))  # noqa: S307 (toy, whitelisted)
    except Exception as err:  # noqa: BLE001
        return f"Error: {err}"


def fake_search(query: str) -> str:
    """A pretend web search. Returns canned 'facts' for a few known queries."""
    knowledge = {
        "molding temperature": "Steering wheel molding runs at 180-220 C.",
        "scrap": "Scrap rate is scrapped units divided by total units, as a percent.",
        "foam volume": "PT55 target foam volume is 8.0 ml.",
    }
    for key, value in knowledge.items():
        if key in query.lower():
            return value
    return "No results found for that query."


TOOLS = {
    "calculator": calculator,
    "search": fake_search,
}

# --- 2. The instructions (the ReAct format contract) ---------------------
# We describe the tools and DEMAND a strict output format. The model fills in
# one step at a time; we stop it before it hallucinates its own Observations.
SYSTEM_PROMPT = """You are a problem-solving agent. Work in a loop using this EXACT format:

Thought: your reasoning about what to do next
Action: the tool to use, one of [calculator, search]
Action Input: the input to the tool

After each Action, you will be given an Observation. Use it to continue.
When you have enough information, respond with:

Thought: I now know the answer
Final Answer: the answer to the user's question

Tools:
- calculator: evaluates a math expression, e.g. "37 / 1250 * 100"
- search: looks up a fact, e.g. "molding temperature"

Only output ONE Thought/Action/Action Input at a time. Do not invent Observations."""


def parse_action(text: str):
    """Pull the Action and Action Input out of the model's reply."""
    action = re.search(r"Action:\s*(.+)", text)
    action_input = re.search(r"Action Input:\s*(.+)", text)
    if action and action_input:
        return action.group(1).strip(), action_input.group(1).strip()
    return None, None


# --- 3. The loop ----------------------------------------------------------
def run_agent(question: str, max_steps: int = 6):
    # temperature=0: we want disciplined, repeatable reasoning steps.
    model = llm.get_llm(temperature=0)

    # The transcript is the model's working memory. It grows each step — this
    # IS the context we engineer and resend every turn.
    transcript = f"{SYSTEM_PROMPT}\n\nQuestion: {question}\n"

    for step in range(1, max_steps + 1):
        # We tell the model to stop as soon as it writes "Observation:" so it
        # can't fabricate the tool result — WE supply real observations.
        reply = model.invoke(transcript, stop=["Observation:"]).content.strip()
        print(f"--- Step {step} ---\n{reply}\n")
        transcript += reply + "\n"

        # Did the model finish?
        if "Final Answer:" in reply:
            answer = reply.split("Final Answer:")[-1].strip()
            print("=== DONE ===")
            print("Final Answer:", answer)
            return answer

        # Otherwise, run the tool it asked for.
        action, action_input = parse_action(reply)
        if action is None:
            print("(No valid Action found — stopping.)")
            return None

        tool_fn = TOOLS.get(action)
        observation = (
            tool_fn(action_input) if tool_fn
            else f"Error: unknown tool '{action}'."
        )
        print(f"Observation: {observation}\n")
        # Feed the real observation back into the context for the next step.
        transcript += f"Observation: {observation}\n"

    print("(Hit max steps without a Final Answer.)")
    return None


if __name__ == "__main__":
    # This needs TWO steps: search for the definition, then calculate the rate.
    question = (
        "We scrapped 37 wheels out of 1250. First look up what scrap rate means, "
        "then calculate it as a percentage."
    )
    print("QUESTION:", question, "\n")
    run_agent(question)

# =========================================================================
# YOUR CHALLENGE (20 min)
# -------------------------------------------------------------------------
# 1. Add a third tool, e.g. `word_count(text)`, register it in TOOLS and the
#    SYSTEM_PROMPT, then ask a question that needs it.
# 2. Ask a pure-math question ("what is 15% of 2400?"). How many steps does the
#    agent take? Does it skip search correctly?
# 3. Remove the stop=["Observation:"] argument and re-run. What goes wrong, and
#    why is controlling the context so important for a reliable agent?
# 4. Compare this to step 04 (single tool call). In your own words: what does
#    the LOOP add that a single call cannot do?
# =========================================================================
