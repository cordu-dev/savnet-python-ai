"""
Step 02 — Conditional Routing & Database Action
===============================================

Concepts:
    1. Conditional Edges: Sometimes the next step depends on the current state.
       LangGraph handles this via `add_conditional_edges`.
    2. Routing Functions: A router function inspects the state and returns a
       string matching the next node to execute.

Scenario:
    We'll build a triage router:
                      /--> [production_expert] --\\
    [START] -> [classifier]                      ---> [END]
                      \\--> [maintenance_expert] -/

    - The `classifier` node uses Mistral to triage the question into "production" or "maintenance".
    - If "production", we route to `production_expert`, which executes a live SQL query
      on our Session 3 Parquet tables!
    - If "maintenance", we route to `maintenance_expert`, which logs a maintenance event.

Run it:
    python 02_conditional_routing.py
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import llm_utils as llm
import db_utils as db

# --- 1. State Definition --------------------------------------------------
class TriageState(TypedDict):
    query: str
    category: str      # "production" or "maintenance"
    sql_query: str     # SQL generated if needed
    response: str      # Answer/Result text
    logs: str          # Execution trace

# --- 2. Node Implementations ----------------------------------------------

def classifier_node(state: TriageState) -> dict:
    """Uses Codestral to categorize the user query."""
    print("-> Executing: classifier_node")
    query = state["query"]
    
    # We ask the LLM to classify. Since we want structured outputs, we instruct it clearly.
    prompt = f"""You are a triage assistant for a manufacturing plant.
Categorize the following user query into exactly one of these two buckets:
- 'production' (if asking about metrics, scrap rates, machine logs, materials, stock or counts)
- 'maintenance' (if asking about repair schedules, downtime, stopping machines, or sensor calibration)

Respond with ONLY the word 'production' or 'maintenance' (lowercase, no punctuation).

Query: {query}"""

    model = llm.get_llm(temperature=0)
    response = model.invoke(prompt).content.strip().lower()
    
    # Simple check in case of unexpected LLM outputs
    category = "production" if "production" in response else "maintenance"
    print(f"   [Classifier Decision] Category: '{category}' (Raw response: '{response}')")
    
    return {
        "category": category,
        "logs": f"classifier: query categorized as '{category}'."
    }


def production_expert_node(state: TriageState) -> dict:
    """Runs a query on our steering wheel manufacturing Parquet database."""
    print("-> Executing: production_expert_node")
    query = state["query"].lower()
    
    # Simple rule-based SQL generator for this concept demo
    # Reuses Parquet data from Session 3!
    sql = ""
    description = ""
    if "quality" in query or "check" in query:
        sql = "SELECT COUNT(*) FROM station_quality_check"
        description = "total quality checks recorded"
    elif "molding" in query:
        sql = "SELECT COUNT(*) FROM station_molding"
        description = "total molding operations"
    else:
        sql = "SELECT COUNT(*) FROM materials_stock"
        description = "items currently in stock"
        
    print(f"   [DB Query] Running: {sql}")
    try:
        results, columns = db.run_query(sql)
        count = results[0][0]
        response = f"Production Expert: Based on database execution, the {description} is {count}."
    except Exception as e:
        response = f"Production Expert: Failed to execute database query. Error: {e}"
        
    return {
        "sql_query": sql,
        "response": response,
        "logs": state.get("logs", "") + "\nproduction_expert: queried Parquet tables."
    }


def maintenance_expert_node(state: TriageState) -> dict:
    """Handles machine maintenance and calibration logging."""
    print("-> Executing: maintenance_expert_node")
    query = state["query"]
    
    # Simple text response for maintenance requests
    response = f"Maintenance Expert: Logged request for: '{query}'. Scheduling support team ticket."
    
    return {
        "response": response,
        "logs": state.get("logs", "") + "\nmaintenance_expert: registered work order."
    }

# --- 3. Routing Function (The Conditional Edge Logic) ---------------------
def route_by_category(state: TriageState) -> str:
    """
    Reads state['category'] and returns the exact node name to route to next.
    """
    category = state["category"]
    if category == "production":
        return "production_expert"
    else:
        return "maintenance_expert"

# --- 4. Building the Graph ------------------------------------------------
builder = StateGraph(TriageState)

# Add all nodes
builder.add_node("classifier", classifier_node)
builder.add_node("production_expert", production_expert_node)
builder.add_node("maintenance_expert", maintenance_expert_node)

# Add start connection
builder.add_edge(START, "classifier")

# Add conditional edge from classifier
# Syntax: add_conditional_edges(source_node, routing_function, mapping_dict)
builder.add_conditional_edges(
    "classifier",
    route_by_category,
    {
        "production": "production_expert",
        "maintenance": "maintenance_expert"
    }
)

# Connect specialist nodes to END
builder.add_edge("production_expert", END)
builder.add_edge("maintenance_expert", END)

# Compile the graph
graph = builder.compile()

# --- 5. Run the Graph with Different Queries ------------------------------
if __name__ == "__main__":
    queries = [
        "How many quality checks do we have registered?",
        "Schedule sensor calibration for molding machine 3 tomorrow."
    ]
    
    for idx, q in enumerate(queries, 1):
        print(f"\n==================== RUN #{idx} ====================")
        print(f"User Query: '{q}'")
        
        final_state = graph.invoke({"query": q})
        
        print("\n--- FINAL STATE RESULT ---")
        print(f"Category: {final_state['category']}")
        if final_state.get('sql_query'):
            print(f"Executed SQL: {final_state['sql_query']}")
        print(f"Response: {final_state['response']}")
        print(f"Logs: {final_state['logs'].replace('\n', ' | ')}")
        print("====================================================")

# =========================================================================
# YOUR CHALLENGE (10 min)
# -------------------------------------------------------------------------
# 1. We want to support a third category: "general_greeting".
#    If the user query is a simple greeting (e.g., "hello", "hi", "hey"), 
#    the classifier should categorize it as "greeting".
# 2. Add a `general_expert` node that responds with a friendly system welcome.
# 3. Add the mapping to the conditional edge, so "greeting" routes to `general_expert`.
# 4. Modify the classifier's prompt to explain this new bucket and run the graph
#    with "Hey there, is anyone online?" to test the routing.
# =========================================================================
