"""
Step 04 — Checkpointing & Human-in-the-Loop
===========================================

Concepts:
    1. Checkpointing: Saving the state of the graph after every node execution.
       This allows us to pause the graph, inspect the state, and resume it.
    2. MemorySaver: An in-memory checkpointer provided by LangGraph for local testing.
    3. Thread Configuration: When executing a graph with checkpointing, we MUST
       provide a `thread_id` in the config dictionary. This separates different
       conversations or execution runs.
    4. Interrupts: Instructing LangGraph to pause execution *before* (or after)
       a specific node, waiting for external human input.

Scenario:
    We'll build a safety-critical maintenance workflow:
    [START] -> [propose_maintenance] -> (Interrupt) -> [execute_maintenance] -> [END]

    - The system proposes a maintenance action (e.g., shutting down a machine).
    - The graph interrupts *before* running `execute_maintenance`.
    - A supervisor reviews the proposed action, approves it, and resumes the graph.

Run it:
    python 04_human_in_the_loop.py
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

# --- 1. State Definition --------------------------------------------------
class MaintenanceState(TypedDict):
    machine_id: str
    action: str
    approved: bool    # Set by human reviewer
    execution_result: str

# --- 2. Node Implementations ----------------------------------------------

def propose_maintenance_node(state: MaintenanceState) -> dict:
    print("-> Executing: propose_maintenance_node")
    machine = state["machine_id"]
    return {
        "action": f"Emergency shutdown and sensor calibration for machine '{machine}'.",
        "approved": False # Default to False, must be overridden by human review
    }


def execute_maintenance_node(state: MaintenanceState) -> dict:
    print("-> Executing: execute_maintenance_node")
    if state.get("approved"):
        result = f"SUCCESS: Dispatched field technician. Action executed: '{state['action']}'"
    else:
        result = "CANCELLED: Maintenance action rejected by supervisor."
        
    return {
        "execution_result": result
    }

# --- 3. Build Graph with Checkpointing and Interrupts ----------------------
builder = StateGraph(MaintenanceState)

builder.add_node("propose_maintenance", propose_maintenance_node)
builder.add_node("execute_maintenance", execute_maintenance_node)

builder.add_edge(START, "propose_maintenance")
builder.add_edge("propose_maintenance", "execute_maintenance")
builder.add_edge("execute_maintenance", END)

# We use an in-memory checkpointer to persist state transitions
memory = MemorySaver()

# Compile the graph. We tell the compiler to INTERRUPT execution BEFORE running "execute_maintenance"
graph = builder.compile(
    checkpointer=memory,
    interrupt_before=["execute_maintenance"]
)

# --- 4. Running the Lifecycle ---------------------------------------------
if __name__ == "__main__":
    # Every checkpointer run needs a thread_id config to locate its state history
    config = {"configurable": {"thread_id": "session_7_demo_thread"}}
    
    # Run the graph for the first time
    print("--- FIRST RUN (Starting execution) ---")
    initial_input = {"machine_id": "Molding-Machine-03"}
    
    # We invoke the graph with the input state and the thread config
    graph.invoke(initial_input, config)
    
    print("\n[PAUSED] Graph execution hit the interrupt boundary before 'execute_maintenance'.")
    
    # Inspect the saved state in the checkpointer
    current_state = graph.get_state(config)
    print(f"Current State Values: {current_state.values}")
    print(f"Next Node to Execute: {current_state.next}") # Will show ('execute_maintenance',)
    
    # --- Simulate Human Intervention ---
    # We will update the state with the supervisor's decision (approving the request)
    # in the checkpointer database.
    print("\n--- HUMAN INTERVENTION: Supervisor reviews and approves ---")
    
    # We write a state update into the exact thread
    graph.update_state(config, {"approved": True}, as_node="propose_maintenance")
    
    # Inspect state again to confirm the update
    updated_state = graph.get_state(config)
    print(f"Updated State Values: {updated_state.values}")
    
    # --- Resume Execution ---
    # To resume, we invoke the graph passing `None` as the input.
    # LangGraph automatically loads the state for "session_7_demo_thread" and continues.
    print("\n--- RESUMING RUN ---")
    final_result = graph.invoke(None, config)
    
    print("\n--- FINAL STATE RESULT ---")
    print(f"Result: {final_result['execution_result']}")

# =========================================================================
# YOUR CHALLENGE (10 min)
# -------------------------------------------------------------------------
# 1. Modify the supervisor review step. Instead of setting `approved` to True
#    directly in the code, use Python's built-in `input()` function to ask
#    the user: "Approve maintenance shutdown? (y/n): ".
# 2. Based on their keyboard input, update the state with `{"approved": True}`
#    or `{"approved": False}`.
# 3. Test running the script twice: once approving, once rejecting. Verify
#    that the final state outputs match the human decision.
# =========================================================================
