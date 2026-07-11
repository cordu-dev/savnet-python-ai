"""
Step 01 — State and Nodes
===========================

Concepts:
    1. Shared State: In LangGraph, the State is the single source of truth.
       It is passed from node to node. We define it here using a `TypedDict`.
    2. Nodes: Nodes are standard Python functions. They take the current state
       as input, perform some operations, and return a dictionary containing
       the updates to the state. They do NOT need to return the entire state,
       only the keys they wish to update.

Scenario:
    We'll build a simple sequential graph:
    [START] -> [clean_query] -> [analyze_query] -> [END]

Run it:
    python 01_state_and_nodes.py
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# --- 1. Define the State Schema -------------------------------------------
# This defines the data structure that will flow through the graph.
class GraphState(TypedDict):
    query: str          # Original question from the user
    cleaned_query: str  # Lowercased and stripped query
    query_length: int   # Character length of the query
    analysis_logs: str  # Trace of what nodes did

# --- 2. Define the Nodes --------------------------------------------------
# Note: Each function accepts `state: GraphState` and returns a dict representing
# updates to the state (matching keys from GraphState).

def clean_query_node(state: GraphState) -> dict:
    """Cleans up the user query input (lowercasing, trimming whitespace)."""
    print("-> Executing: clean_query_node")
    raw_query = state["query"]
    cleaned = raw_query.strip().lower()
    
    # We return updates. LangGraph will merge this dictionary into the main state.
    return {
        "cleaned_query": cleaned,
        "analysis_logs": "clean_query_node: success."
    }


def analyze_query_node(state: GraphState) -> dict:
    """Analyzes properties of the cleaned query."""
    print("-> Executing: analyze_query_node")
    cleaned = state["cleaned_query"]
    length = len(cleaned)
    
    # We append to the logs and record the length
    current_logs = state.get("analysis_logs", "")
    new_logs = current_logs + "\nanalyze_query_node: calculated query length."
    
    return {
        "query_length": length,
        "analysis_logs": new_logs
    }

# --- 3. Build and Compile the Graph ----------------------------------------
builder = StateGraph(GraphState)

# Add our nodes to the builder graph
builder.add_node("clean_query", clean_query_node)
builder.add_node("analyze_query", analyze_query_node)

# Connect the nodes sequentially
builder.add_edge(START, "clean_query")
builder.add_edge("clean_query", "analyze_query")
builder.add_edge("analyze_query", END)

# Compile into a runnable graph object
graph = builder.compile()

# --- 4. Invoke the Graph ---------------------------------------------------
if __name__ == "__main__":
    # Test query with extra whitespace and caps
    input_data = {"query": "  Check Mold Machine 5 TEMP!   "}
    
    print("Starting graph run...")
    print(f"Input State: {input_data}\n")
    
    final_state = graph.invoke(input_data)
    
    print("\n--- FINAL STATE RESULT ---")
    print(f"Original Query:  '{final_state['query']}'")
    print(f"Cleaned Query:   '{final_state['cleaned_query']}'")
    print(f"Query Length:    {final_state['query_length']} characters")
    print("\nLogs Trace:")
    print(final_state["analysis_logs"])

# =========================================================================
# YOUR CHALLENGE (10 min)
# -------------------------------------------------------------------------
# 1. Modify the `clean_query_node` to strip out punctuation (like '!', '?',
#    or '.'). Test it by running the script with the query:
#    "Is molding machine 3 online?"
# 2. Add an intermediate node `sentiment_detector_node`. If the query contains
#    words like "emergency", "temp", "stop", or "broken", set a new State key:
#    `is_urgent: bool` to True, otherwise False.
#    Remember to update the `GraphState` TypedDict to include `is_urgent`.
# 3. Wire `sentiment_detector_node` into the sequence:
#    [clean_query] -> [sentiment_detector] -> [analyze_query]
# =========================================================================
