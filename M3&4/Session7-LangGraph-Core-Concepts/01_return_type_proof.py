import sys
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# Define a simple state schema
class SimpleState(TypedDict):
    message: str
    counter: int

# =====================================================================
# 1. NODE DEFINITIONS
# =====================================================================

def update_node(state: SimpleState) -> dict:
    """Case 1: Returns a dictionary containing updates to specific keys.
    This is the standard and correct way to update state.
    """
    print("\n[Node 1] Executing update_node...")
    # We only return the key we want to change. LangGraph merges it.
    return {"message": state["message"] + " -> updated!"}


def side_effect_node(state: SimpleState) -> None:
    """Case 2: Returns None (or has no return statement).
    Used for side-effects like logging or calling external APIs.
    The state remains unchanged.
    """
    print("\n[Node 2] Executing side_effect_node...")
    print(f"         Read State: message='{state['message']}', counter={state['counter']}")
    print("         (Doing side-effects but returning None)")
    # No return statement = returns None


def invalid_node(state: SimpleState) -> str:
    """Case 3: Returns a raw string instead of a dictionary.
    This is INVALID because LangGraph doesn't know which state key to assign this to.
    """
    print("\n[Node 3] Executing invalid_node...")
    return "This is a raw string!"


# =====================================================================
# 2. RUNNING THE PROOFS
# =====================================================================

def run_valid_proof():
    print("=== PROOF 1: Running Graph with Dict & None Return Types ===")
    
    # Create the graph
    builder = StateGraph(SimpleState)
    builder.add_node("step_one", update_node)
    builder.add_node("step_two", side_effect_node)
    
    builder.add_edge(START, "step_one")
    builder.add_edge("step_one", "step_two")
    builder.add_edge("step_two", END)
    
    graph = builder.compile()
    
    # Run the graph
    initial_state = {"message": "Hello class", "counter": 10}
    print(f"Initial State: {initial_state}")
    
    final_state = graph.invoke(initial_state)
    print(f"\nFinal State: {final_state}")
    print("============================================================\n")

    print(graph.get_graph().draw_ascii())


def run_invalid_proof():
    print("=== PROOF 2: Running Graph with Invalid String Return Type ===")
    
    builder = StateGraph(SimpleState)
    builder.add_node("invalid_step", invalid_node)
    builder.add_edge(START, "invalid_step")
    builder.add_edge("invalid_step", END)
    
    graph = builder.compile()
    
    initial_state = {"message": "Hello class", "counter": 10}
    
    print(graph.get_graph().draw_ascii())

    try:
        graph.invoke(initial_state)
    except Exception as e:
        print(f"\n❌ CAUGHT EXPECTED ERROR:")
        print(f"   Error Type: {type(e).__name__}")
        print(f"   Error Message: {e}")
    print("============================================================\n")
# =====================================================================
# 3. CHALLENGE: AgentState Counter Update
# =====================================================================

class AgentState(TypedDict):
    chat_history: list
    attempts: int


def increment_attempts_node(state: AgentState) -> dict:
    """Challenge Node: Increments attempts by 1.
    Note that we DO NOT return or touch chat_history here!
    """
    print("\n[Challenge Node] Executing increment_attempts_node...")
    # Read the current attempts, increment, and return just the update
    return {"attempts": state["attempts"] + 1}


def run_challenge_proof():
    print("=== PROOF 3: Updating a Counter without touching other keys ===")
    
    builder = StateGraph(AgentState)
    builder.add_node("increment_attempts", increment_attempts_node)
    builder.add_edge(START, "increment_attempts")
    builder.add_edge("increment_attempts", END)
    
    graph = builder.compile()
    
    initial_state = {
        "chat_history": ["User: Hello", "Agent: Hi there!"],
        "attempts": 0
    }
    print(f"Initial Agent State: {initial_state}")
    
    final_state = graph.invoke(initial_state)
    print(f"\nFinal Agent State: {final_state}")
    print("============================================================\n")


if __name__ == "__main__":
    run_valid_proof()
    run_invalid_proof()
    run_challenge_proof()
