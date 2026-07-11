"""
Step 00 — Does my LangGraph setup work?
=========================================

Goal:
    Ensure that we can import langgraph, compile a minimal StateGraph,
    and verify that our API keys are loaded.

Run it:
    python 00_setup_check.py

Prerequisites:
    - Activate your virtual environment.
    - Run: `pip install langgraph`
    - Copy your .env from Session 6 (or copy .env.example to .env and insert key).
"""

import sys
from typing import TypedDict

# --- 1. Check LangGraph Import --------------------------------------------
try:
    import langgraph
    from langgraph.graph import StateGraph, START, END
    print(f"Step 1/3: LangGraph package imported successfully (v{langgraph}).")
except ImportError:
    print("\n[ERROR] LangGraph is not installed!")
    print("Please run: pip install langgraph")
    sys.exit(1)

# --- 2. Check Mistral LLM Configuration -----------------------------------
try:
    import llm_utils as llm
    llm.check_key()
    model = llm.get_llm(temperature=0)
    print("Step 2/3: Mistral API key and model verified.")
except Exception as err:
    print(f"\n[ERROR] Mistral setup failed: {err}")
    sys.exit(1)

# --- 3. Build a Minimal StateGraph -----------------------------------------
# In LangGraph, everything revolves around STATE.
# State is defined using a standard Python type (like a TypedDict).
class SimpleState(TypedDict):
    message: str

# Define a single, simple node function. 
# A node takes the current state, performs an action, and returns updated state keys.
def hello_node(state: SimpleState) -> dict:
    print(" -> Executing hello_node...")
    return {"message": state["message"] + " ...and welcome to LangGraph!"}

try:
    # 1. Initialize the StateGraph with our state schema
    builder = StateGraph(SimpleState)
    
    # 2. Add the node to the graph
    builder.add_node("hello", hello_node)
    
    # 3. Define the connections (edges)
    # START is a special builtin indicator that tells the graph where to begin
    builder.add_edge(START, "hello")
    # END indicates the execution should terminate after this node
    builder.add_edge("hello", END)
    
    # 4. Compile the builder into a runnable Graph
    graph = builder.compile()
    print("Step 3/3: Minimal StateGraph compiled successfully.")
    
    # Run the graph!
    initial_state = {"message": "Hello class"}
    print(f"\nInvoking graph with input: {initial_state}")
    result = graph.invoke(initial_state)
    print(f"Resulting state: {result}")

    print(graph.get_graph().draw_ascii())
    
    print("\n🎉 Setup successful! You are ready to start with 01_state_and_nodes.py.")
    
except Exception as err:
    print(f"\n[ERROR] Graph compilation/execution failed: {err}")
    sys.exit(1)

# =========================================================================
# YOUR CHALLENGE (5 min)
# -------------------------------------------------------------------------
# 1. Print the graph structure using ASCII by calling:
#    `print(graph.get_graph().draw_ascii())`
# 2. Add a second node called "farewell" that appends " Goodbye!" to the 
#    message state key. Connect "hello" to "farewell", and "farewell" to END.
# 3. Run the modified graph. Does it run sequentially?
# =========================================================================
