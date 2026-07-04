"""
Step 04 — Tool calling (giving the LLM functions)
=================================================

Big idea:
    An LLM can't do math reliably, doesn't know today's date, and can't read
    your database. But it CAN decide to "call a tool" — a plain Python function
    you provide — and then use the result.

    You: "here are some functions you may use."
    LLM: "for this question, please run add(3, 4)."
    You: run it, send back "7".
    LLM: writes the final answer using that 7.

The model never runs your code itself. It only REQUESTS a call; YOUR program
executes it and returns the result. That control is what makes agents safe(ish).

This is the seed of every agent in this course: the LLM chooses actions, your
code performs them.

Run it:
    python 04_tool_calling.py
"""

from langchain_core.tools import tool

import llm_utils as llm


# --- 1. Define tools ------------------------------------------------------
# The @tool decorator turns a normal function into something the LLM can see.
# The docstring is CRITICAL: the model reads it to decide when to use the tool.
@tool
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together and return the product."""
    return a * b


@tool
def scrap_rate(scrapped: int, total: int) -> float:
    """Compute scrap rate as a percentage: scrapped units out of total units."""
    return round((scrapped / total) * 100, 2)


tools = [multiply, scrap_rate]
tools_by_name = {t.name: t for t in tools}

# --- 2. Bind the tools to the model --------------------------------------
# bind_tools tells the model which functions exist and what arguments they take.
model = llm.get_llm(temperature=0)
model_with_tools = model.bind_tools(tools)

question = "Out of 1,250 wheels we scrapped 37. What's the scrap rate percentage?"
print("Question:", question, "\n")

# --- 3. First call: the model decides which tool to call -----------------
ai_msg = model_with_tools.invoke(question)

if not ai_msg.tool_calls:
    # The model answered directly without needing a tool.
    print("Model answered without a tool:", ai_msg.content)
else:
    # ai_msg.tool_calls is a list of requested calls (name + arguments).
    for call in ai_msg.tool_calls:
        print(f"Model wants to call: {call['name']}({call['args']})")

        # --- 4. WE execute the tool ---------------------------------------
        chosen = tools_by_name[call["name"]]
        output = chosen.invoke(call["args"])
        print("We ran it. Result =", output)

    # --- 5. Send the result back so the model can phrase a final answer ---
    from langchain_core.messages import HumanMessage, ToolMessage

    followup = [HumanMessage(content=question), ai_msg]
    for call in ai_msg.tool_calls:
        result = tools_by_name[call["name"]].invoke(call["args"])
        followup.append(ToolMessage(content=str(result), tool_call_id=call["id"]))

    final = model_with_tools.invoke(followup)
    print("\nFinal answer:", final.content.strip())

# =========================================================================
# YOUR CHALLENGE (15 min)
# -------------------------------------------------------------------------
# 1. Add a `divide` tool and ask a question that needs it. Does the model pick
#    the right tool on its own?
# 2. Ask a question that needs NO tool ("what's a steering wheel?"). Confirm
#    tool_calls is empty and it just answers.
# 3. Break a tool's docstring (make it vague or wrong). Does the model still
#    choose it correctly? What does that teach you about writing tool docs?
# =========================================================================
