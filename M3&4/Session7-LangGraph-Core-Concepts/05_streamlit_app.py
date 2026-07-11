"""
Step 05 — Streamlit LangGraph Interactive Dashboard
===================================================

This dashboard demonstrates all core LangGraph concepts in a live user interface.
It compiles a graph that:
1. Classifies the query (using Mistral).
2. Routes to the appropriate specialist:
   - Production: Queries the real Session 3 Parquet database via DuckDB.
   - Maintenance: Proposes a machine action, and then halts for human approval.
   - General: Responds to greetings.
3. Renders the graph structure dynamically using Mermaid.ink.

Run it:
    streamlit run 05_streamlit_app.py
"""

import streamlit as st
import operator
import base64
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

import llm_utils as llm
import db_utils as db

# --- 1. Define the LangGraph State Schema ----------------------------------
class MasterState(TypedDict):
    query: str
    category: str      # "production", "maintenance", "general"
    sql_query: str     # SQL run by production expert (if any)
    action_proposed: str  # Action proposed by maintenance (if any)
    approved: bool     # Approved by human supervisor
    response: str      # Final system answer
    execution_trace: Annotated[list[str], operator.add] # Log node visits

# --- 2. Define Node Functions ----------------------------------------------

def classifier_node(state: MasterState) -> dict:
    """Uses Mistral to triage the user request."""
    query = state["query"]
    prompt = f"""You are a triage assistant for a manufacturing plant.
Categorize the following user query into exactly one of these three buckets:
- 'production' (if asking about metrics, scrap rates, machine logs, materials, stock or counts)
- 'maintenance' (if asking about repair schedules, downtime, stopping machines, or sensor calibration)
- 'general' (if the query is a simple greeting like hello, hi, or about who you are)

Respond with ONLY the word 'production', 'maintenance', or 'general' (lowercase, no punctuation).

Query: {query}"""

    try:
        model = llm.get_llm(temperature=0)
        category = model.invoke(prompt).content.strip().lower()
        if category not in ["production", "maintenance", "general"]:
            category = "general"
    except Exception:
        # Fallback to simple rule-based classification if API fails
        q_lower = query.lower()
        if any(w in q_lower for w in ["check", "scrap", "molding", "quality", "conductor", "foaming", "laser", "materials", "stock"]):
            category = "production"
        elif any(w in q_lower for w in ["repair", "schedule", "calibrate", "stop", "maintenance", "downtime"]):
            category = "maintenance"
        else:
            category = "general"
            
    return {
        "category": category,
        "execution_trace": [f"classifier_node: query categorized as '{category}'"]
    }


def production_expert_node(state: MasterState) -> dict:
    """Runs a live SQL query on Parquet files based on the query."""
    query = state["query"].lower()
    
    # Generate simple SQL based on keyword detection
    sql = ""
    description = ""
    if "quality" in query or "check" in query:
        sql = "SELECT COUNT(*) FROM station_quality_check"
        description = "total quality checks recorded in parquet"
    elif "molding" in query:
        sql = "SELECT COUNT(*) FROM station_molding"
        description = "total molding operations registered"
    elif "foaming" in query:
        sql = "SELECT COUNT(*) FROM station_foaming"
        description = "total foaming operations registered"
    elif "conductor" in query:
        sql = "SELECT COUNT(*) FROM station_conductor"
        description = "total conductor installations"
    elif "laser" in query:
        sql = "SELECT COUNT(*) FROM station_laser"
        description = "total laser welding operations"
    elif "materials" in query or "stock" in query:
        sql = "SELECT COUNT(*) FROM materials_stock"
        description = "materials currently in stock"
    else:
        sql = "SELECT COUNT(*) FROM materials_log"
        description = "material logs in historical archive"
        
    try:
        results, _ = db.run_query(sql)
        count = results[0][0]
        response = f"📊 Production Agent: Found **{count}** {description} in the database."
    except Exception as e:
        response = f"⚠️ Production Agent: Tried running query `{sql}` but got database error: {e}"
        
    return {
        "sql_query": sql,
        "response": response,
        "execution_trace": [f"production_expert_node: ran query `{sql}`"]
    }


def maintenance_proposer_node(state: MasterState) -> dict:
    """Proposes a maintenance action that requires human clearance."""
    query = state["query"]
    
    # Extract machine or action
    action = f"Emergency machine intervention requested. Details: {query}"
    
    return {
        "action_proposed": action,
        "approved": False, # Explicitly false until supervisor clicks Approve
        "response": "Awaiting supervisor approval for safety-critical maintenance.",
        "execution_trace": ["maintenance_proposer_node: action proposed, entering gate"]
    }


def maintenance_executor_node(state: MasterState) -> dict:
    """Executes the maintenance action only if approved is True."""
    is_approved = state.get("approved", False)
    action = state.get("action_proposed", "No action specified")
    
    if is_approved:
        response = f"⚙️ Maintenance Agent: **ACTION DISPATCHED!** ✅\nDetail: '{action}' has been successfully scheduled."
        trace = "maintenance_executor_node: action executed"
    else:
        response = f"⚙️ Maintenance Agent: **ACTION CANCELLED!** ❌\nDetail: '{action}' was rejected by the supervisor."
        trace = "maintenance_executor_node: action rejected and cancelled"
        
    return {
        "response": response,
        "execution_trace": [trace]
    }


def general_expert_node(state: MasterState) -> dict:
    """Handles conversational greetings."""
    response = "👋 Hello! I am the factory floor supervisor agent. Ask me production questions (from parquet data) or schedule machine maintenance."
    return {
        "response": response,
        "execution_trace": ["general_expert_node: answered greeting"]
    }

# --- 3. Routing Condition --------------------------------------------------
def route_classifier(state: MasterState) -> str:
    category = state.get("category", "general")
    if category == "production":
        return "production_expert"
    elif category == "maintenance":
        return "maintenance_proposer"
    else:
        return "general_expert"

# --- 4. Assemble and Compile the Graph -------------------------------------
@st.cache_resource
def get_compiled_graph():
    builder = StateGraph(MasterState)
    
    # Add nodes
    builder.add_node("classifier", classifier_node)
    builder.add_node("production_expert", production_expert_node)
    builder.add_node("maintenance_proposer", maintenance_proposer_node)
    builder.add_node("maintenance_executor", maintenance_executor_node)
    builder.add_node("general_expert", general_expert_node)
    
    # Wire edges
    builder.add_edge(START, "classifier")
    
    # Conditional edge
    builder.add_conditional_edges(
        "classifier",
        route_classifier,
        {
            "production": "production_expert",
            "maintenance": "maintenance_proposer",
            "general": "general_expert"
        }
    )
    
    # Maintenance sequence
    builder.add_edge("maintenance_proposer", "maintenance_executor")
    
    # Connect leaf nodes to END
    builder.add_edge("production_expert", END)
    builder.add_edge("general_expert", END)
    builder.add_edge("maintenance_executor", END)
    
    # Use MemorySaver checkpointer for thread history
    memory = MemorySaver()
    
    # Interrupt execution BEFORE executing the maintenance executor node
    graph = builder.compile(
        checkpointer=memory,
        interrupt_before=["maintenance_executor"]
    )
    return graph

# Initialize the graph
graph = get_compiled_graph()

# --- 5. Streamlit Page Setup ------------------------------------------------
st.set_page_config(page_title="Session 7: LangGraph Core Concepts", page_icon="⚙️", layout="wide")

# Theme styling & title
st.markdown("""
    <style>
        .main-title { font-size: 38px; font-weight: 700; color: #1E3A8A; margin-bottom: 2px; }
        .sub-title { font-size: 16px; color: #4B5563; margin-bottom: 25px; }
        .metric-card { background-color: #F3F4F6; border-radius: 8px; padding: 15px; border-left: 5px solid #3B82F6; }
        .log-box { font-family: monospace; font-size: 12px; background-color: #1F2937; color: #10B981; padding: 10px; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Session 7 · LangGraph Orchestrator 🕸️</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Learn State Graphs, Routing, and Human-in-the-Loop gates on top of the steering wheel dataset.</div>', unsafe_allow_html=True)

# Generate Session variables to keep track of active run and thread IDs
if "thread_id" not in st.session_state:
    import uuid
    st.session_state.thread_id = str(uuid.uuid4())[:8]

if "exec_logs" not in st.session_state:
    st.session_state.exec_logs = []

if "latest_state" not in st.session_state:
    st.session_state.latest_state = None

config = {"configurable": {"thread_id": st.session_state.thread_id}}

# --- 6. Sidebar: Graph Visualizer ------------------------------------------
with st.sidebar:
    st.header("Graph Architecture")
    st.caption("Rendered dynamically from code using Mermaid.ink")
    
    # Get Mermaid code and encode for Mermaid.ink
    try:
        mermaid_code = graph.get_graph().draw_mermaid()
        encoded = base64.b64encode(mermaid_code.encode("utf-8")).decode("utf-8")
        image_url = f"https://mermaid.ink/img/{encoded}"
        st.image(image_url, use_container_width=True)
    except Exception as e:
        st.info("Compile check: Pygraphviz / Mermaid rendering error, displaying raw code:")
        st.code(graph.get_graph().draw_mermaid(), language="mermaid")
        
    st.markdown("---")
    st.markdown("""
    ### Key Concepts Covered
    * **State Graph:** Manages overall execution data structure.
    * **Routing:** Triaged by a Mistral Classifier.
    * **Session 3 Database:** Live counts performed in DuckDB by the production expert.
    * **Human-in-the-Loop:** Safety interrupts before executing maintenance actions.
    """)
    
    if st.button("🔄 Reset Thread ID"):
        st.session_state.thread_id = str(uuid.uuid4())[:8]
        st.session_state.exec_logs = []
        st.session_state.latest_state = None
        st.rerun()

# --- 7. Main Panel: Form Inputs & Execution ---------------------------------
col_input, col_state = st.columns([2, 1])

with col_input:
    st.subheader("Send Query to Factory Assistant")
    
    # Provide helpful quick buttons
    st.write("Suggested queries:")
    col_q1, col_q2, col_q3 = st.columns(3)
    preset_query = ""
    if col_q1.button("📊 Row count of quality check table", use_container_width=True):
        preset_query = "How many quality checks do we have registered in parquet?"
    if col_q2.button("🔧 Stop molding machine 3 for calibration", use_container_width=True):
        preset_query = "Schedule shutdown for Machine 3 immediately!"
    if col_q3.button("👋 Say hello to the supervisor", use_container_width=True):
        preset_query = "Hi, who are you?"
        
    # Text input
    user_query = st.text_input("Enter your factory floor request:", value=preset_query, placeholder="What would you like the graph to process?")
    
    # Check if API Key works
    key_working = True
    try:
        llm.check_key()
    except RuntimeError:
        st.warning("⚠️ No `MISTRAL_API_KEY` detected in `.env`. The app will fallback to simple regex matching.")
        key_working = False

    if st.button("⚡ Run LangGraph", type="primary", use_container_width=True):
        if user_query:
            # We starting a new run in the thread. Let's clear previous logs.
            st.session_state.exec_logs = [f"Initial trigger. Thread ID: {st.session_state.thread_id}"]
            
            # Invoke the graph. It will run until either END is reached, or it hits the INTERRUPT before maintenance_executor.
            with st.status("Graph processing...", expanded=True) as status:
                st.write("1. Initializing Graph Input State...")
                
                # Streaming updates node-by-node
                for chunk in graph.stream({"query": user_query}, config):
                    for node_name, node_state in chunk.items():
                        st.write(f"Executing Node: `{node_name}`")
                        st.session_state.exec_logs.append(f"Node '{node_name}' finished execution.")
                        if "execution_trace" in node_state:
                            for trace in node_state["execution_trace"]:
                                st.session_state.exec_logs.append(f"  -> Trace: {trace}")
                
                status.update(label="Graph Execution Halted / Finished", state="complete")
                
            # Get latest state values
            graph_state = graph.get_state(config)
            st.session_state.latest_state = graph_state
            st.rerun()

    # --- Check for Interrupt Gate (Human-in-the-Loop) ---
    if st.session_state.latest_state:
        state_vals = st.session_state.latest_state.values
        next_nodes = st.session_state.latest_state.next
        
        # If the next node to execute is "maintenance_executor", we are interrupted!
        if "maintenance_executor" in next_nodes:
            st.markdown("---")
            st.warning("⚠️ **SAFETY INTERRUPT TRIPPED**")
            st.markdown(f"""
            **The graph is currently paused.** An automated agent has proposed a safety-critical operation:
            * **Proposed Action:** `{state_vals.get('action_proposed')}`
            * **Target System:** Maintenance Scheduler
            
            Please approve or reject this request below.
            """)
            
            col_app, col_rej = st.columns(2)
            
            if col_app.button("✅ Approve and Dispatch Action", type="primary", use_container_width=True):
                # Update state in checkpointer with approved = True
                graph.update_state(config, {"approved": True}, as_node="maintenance_proposer")
                st.session_state.exec_logs.append("Human-in-the-loop: Action approved by supervisor.")
                
                # Resume execution
                with st.status("Resuming graph...", expanded=True) as status:
                    for chunk in graph.stream(None, config):
                        for node_name, node_state in chunk.items():
                            st.write(f"Resuming Node: `{node_name}`")
                            st.session_state.exec_logs.append(f"Node '{node_name}' finished execution.")
                            if "execution_trace" in node_state:
                                for trace in node_state["execution_trace"]:
                                    st.session_state.exec_logs.append(f"  -> Trace: {trace}")
                    status.update(label="Resumed execution complete.", state="complete")
                
                # Update saved state
                st.session_state.latest_state = graph.get_state(config)
                st.rerun()
                
            if col_rej.button("❌ Reject and Cancel Action", type="secondary", use_container_width=True):
                # Update state with approved = False
                graph.update_state(config, {"approved": False}, as_node="maintenance_proposer")
                st.session_state.exec_logs.append("Human-in-the-loop: Action rejected by supervisor.")
                
                # Resume execution
                with st.status("Resuming graph...", expanded=True) as status:
                    for chunk in graph.stream(None, config):
                        for node_name, node_state in chunk.items():
                            st.write(f"Resuming Node: `{node_name}`")
                            st.session_state.exec_logs.append(f"Node '{node_name}' finished execution.")
                            if "execution_trace" in node_state:
                                for trace in node_state["execution_trace"]:
                                    st.session_state.exec_logs.append(f"  -> Trace: {trace}")
                    status.update(label="Resumed execution complete.", state="complete")
                
                # Update saved state
                st.session_state.latest_state = graph.get_state(config)
                st.rerun()

        # Display Response if finished
        elif not next_nodes and "response" in state_vals:
            st.markdown("---")
            st.success("🏁 **Response Received**")
            st.markdown(state_vals["response"])
            if state_vals.get("sql_query"):
                st.info(f"Executed SQL Query: `{state_vals['sql_query']}`")

# --- 8. Right Panel: Active State Inspector ---------------------------------
with col_state:
    st.subheader("Graph State Inspector")
    if st.session_state.latest_state:
        vals = st.session_state.latest_state.values
        next_steps = st.session_state.latest_state.next
        
        # Display metadata
        st.write(f"**Thread ID:** `{st.session_state.thread_id}`")
        st.write(f"**Next Node to Run:** `{next_steps if next_steps else 'FINISHED (END)'}`")
        
        # JSON viewer of the current keys in state
        st.json(vals)
    else:
        st.info("Run a query to view state details.")
        
    st.subheader("Console Execution Logs")
    if st.session_state.exec_logs:
        log_content = "\n".join(st.session_state.exec_logs)
        st.markdown(f'<div class="log-box">{log_content.replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
    else:
        st.caption("No logs yet.")
