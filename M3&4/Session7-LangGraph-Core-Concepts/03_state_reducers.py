"""
Step 03 — State Reducers (Aggregating History)
==============================================

Concepts:
    1. Overwrite (Default): By default, LangGraph updates state keys by overwriting
       them. If Node A returns `{"logs": "A finished"}` and Node B returns 
       `{"logs": "B finished"}`, the value of "logs" becomes "B finished".
    2. Reducers: If we want to append lists, accumulate values, or merge dictionaries
       rather than replace them, we use Python's `typing.Annotated` combined with a
       reducer function.
    3. `operator.add`: A common reducer. When applied to lists, it appends the new
       items to the existing list.

Scenario:
    We'll build a parallel/multi-step logging graph where multiple nodes append to
    a shared `execution_log` list:
    [START] -> [node_a] -> [node_b] -> [node_c] -> [END]

Run it:
    python 03_state_reducers.py
"""

import operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END

# --- 1. State Definition with a Reducer ------------------------------------
# We annotate the `execution_log` field with a reducer function.
# Here, `operator.add` acts on lists. If node returns `{"execution_log": ["x"]}`,
# it will be appended to the current list rather than overwriting it.
class ReducedState(TypedDict):
    query: str
    
    # By using Annotated and operator.add, lists will be combined (appended)
    execution_log: Annotated[list[str], operator.add]
    
    # Without annotations, normal keys get overwritten
    last_node_executed: str 

# --- 2. Node Implementations ----------------------------------------------

def node_a(state: ReducedState) -> dict:
    print("-> Executing: node_a")
    return {
        "execution_log": ["Node A started processing."], # Returns a list
        "last_node_executed": "node_a"
    }

def node_b(state: ReducedState) -> dict:
    print("-> Executing: node_b")
    return {
        "execution_log": ["Node B query lookup complete."], # Appends to list
        "last_node_executed": "node_b"
    }

def node_c(state: ReducedState) -> dict:
    print("-> Executing: node_c")
    return {
        "execution_log": ["Node C output formatting complete."], # Appends to list
        "last_node_executed": "node_c"
    }

# --- 3. Graph Assembly -----------------------------------------------------
builder = StateGraph(ReducedState)

builder.add_node("node_a", node_a)
builder.add_node("node_b", node_b)
builder.add_node("node_c", node_c)

builder.add_edge(START, "node_a")
builder.add_edge("node_a", "node_b")
builder.add_edge("node_b", "node_c")
builder.add_edge("node_c", END)

graph = builder.compile()

# --- 4. Invoking the Graph -------------------------------------------------
if __name__ == "__main__":
    initial_input = {
        "query": "Check system uptime",
        "execution_log": ["Triggered from main script."] # Initial list value
    }
    
    print("Running graph run with state reducers...")
    result = graph.invoke(initial_input)
    
    print("\n--- FINAL STATE RESULT ---")
    print(f"Last Node Executed: {result['last_node_executed']}")
    print("\nExecution Log History (Aggregated via operator.add):")
    for i, log in enumerate(result["execution_log"], 1):
        print(f"  {i}. {log}")
        
    print("\n💡 Observe how 'last_node_executed' was overwritten and only shows the final node,")
    print("while 'execution_log' accumulated entries from every single node along the way!")

# =========================================================================
# YOUR CHALLENGE (10 min)
# -------------------------------------------------------------------------
# 1. Let's write a custom reducer function instead of `operator.add`.
#    Write a function `unique_logger(existing: list, new: list) -> list`
#    that combines two lists but removes any duplicate strings.
# 2. Modify the State to use your `unique_logger` reducer instead of `operator.add`.
# 3. Add duplicate logs inside your nodes and verify that the final state contains
#    only unique entries.
# =========================================================================
