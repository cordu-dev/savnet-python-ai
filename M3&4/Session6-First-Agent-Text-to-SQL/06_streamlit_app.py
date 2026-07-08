"""
Step 06 — Final Streamlit App: Text-to-SQL Manufacturing Agent
=============================================================

Goal:
    This is the capstone of Session 6. We assemble all the concepts learned
    so far (Schema Extraction, SQL Generation, Safety Guardrails, Self-Correction
    Loops, and Plain-English Explanations) into a high-fidelity, interactive
    dashboard.

    The supervisor can ask questions in natural language, watch the agent
    "think" and write SQL in real-time, inspect the safety validation, view
    the raw data, and read the plain-English synthesis.

Run it:
    streamlit run 06_streamlit_app.py
"""

import re
import duckdb
import pandas as pd
import streamlit as st
import plotly.express as px

import llm_utils as llm
import db_utils

# --- Page Setup & Premium Styling ----------------------------------------
st.set_page_config(
    page_title="FactorySQL Agent · ZF Life",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics and dark theme accentuation
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Space+Grotesk:wght@400;700&display=swap');
    
    /* Font configurations */
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    /* Custom Header Gradient */
    .header-container {
        background: linear-gradient(135deg, #1f1c2c 0%, #928dab 100%);
        padding: 2.5rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .header-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        background: linear-gradient(to right, #ffffff, #e0e0e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.85;
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: transform 0.2s ease-in-out;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.15);
    }
</style>
""", unsafe_allow_html=True)

# --- Prompts --------------------------------------------------------------
SQL_PROMPT = """You are a DuckDB SQL expert. Given the database schema below, write a single valid SQL query that answers the user's question.

Database Schema Context:
{schema_context}

Rules:
1. Return ONLY the raw SQL query. Do not add any conversational text.
2. Do not wrap the SQL query in markdown blocks (e.g., do not use ```sql ... ```).
3. Only use tables and columns defined in the schema.
4. Ensure the query is compatible with DuckDB SQL.
"""

EXPLANATION_PROMPT = """You are an expert manufacturing data analyst.
Explain the database query results below to a factory supervisor in clear, plain English.

Original Question: {question}
SQL Query Run: {sql_query}
Query Results:
{results_str}

Guidelines for your explanation:
1. Directly answer the user's question in the first sentence.
2. Briefly explain *how* the data was gathered (e.g. "We joined molding logs with quality logs...").
3. Point out any interesting findings.
4. List any critical caveats (e.g. "This only counts PT77 since it is the only type passing the laser station").
5. Format your output using clean Markdown, with bolding and bullet points where helpful.
"""

# --- Helper Functions -----------------------------------------------------
def clean_sql(raw_sql: str) -> str:
    """Extracts raw SQL from markdown blocks if the LLM wraps it."""
    match = re.search(r"```sql\s+(.*?)\s*```", raw_sql, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"```\s+(.*?)\s*```", raw_sql, re.DOTALL)
    if match:
        return match.group(1).strip()
    return raw_sql.strip()


def validate_sql(sql_query: str) -> tuple[bool, str]:
    """Validates the generated SQL for safety and table access boundaries."""
    query_upper = sql_query.upper().strip()
    
    if not (query_upper.startswith("SELECT") or query_upper.startswith("WITH")):
        return False, "Query must be read-only (start with SELECT or WITH)."
        
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "REPLACE"]
    words = re.findall(r"\b[A-Z]+\b", query_upper)
    for word in words:
        if word in forbidden:
            return False, f"Forbidden database write command detected: {word}."
            
    # Check for direct file queries or system catalogs
    if "read_parquet" in query_upper.lower():
        return False, "Direct reads of parquet files are disabled. Use the registered table views."
        
    return True, ""


# --- Main Agent Pipeline --------------------------------------------------
def run_agent_pipeline(question: str, con: duckdb.DuckDBPyConnection, schema: str):
    """
    Executes the full agent workflow with real-time status updates in Streamlit.
    """
    model = llm.get_llm(temperature=0.0)
    
    # We use st.status to create an interactive log of the agent's work
    with st.status("Agent processing request...", expanded=True) as status:
        
        # Step 1: Extract Schema
        status.update(label="Analyzing database schema...")
        # (Schema is preloaded in streamlit state, already fetched)
        st.write("✓ Extracted schema parameters for 8 manufacturing stations.")
        
        # Step 2: Generate initial SQL
        status.update(label="Drafting SQL query with Mistral Codestral...")
        prompt = SQL_PROMPT.format(schema_context=schema)
        messages = [
            ("system", prompt),
            ("user", f"Question: {question}")
        ]
        response = model.invoke(messages)
        sql = clean_sql(response.content)
        st.write("✓ SQL query generated successfully.")
        
        # Step 3: Validate SQL
        status.update(label="Running guardrail validations...")
        is_valid, error_msg = validate_sql(sql)
        if not is_valid:
            status.update(label="Safety Validation Failed ✗", state="error")
            st.error(f"Validation Error: {error_msg}")
            return None, None, None
        st.write("✓ Safety check complete. SQL approved.")
        
        # Step 4: Execute & Correct Loop
        status.update(label="Executing query on DuckDB...")
        max_attempts = 3
        attempt = 1
        results_df = None
        
        while attempt <= max_attempts:
            try:
                results_df = con.execute(sql).fetchdf()
                st.write(f"✓ DuckDB query executed. Row count: {len(results_df)}")
                break
            except Exception as e:
                db_err = str(e)
                st.warning(f"Database error on Attempt {attempt}: {db_err}")
                if attempt == max_attempts:
                    status.update(label="Agent execution failed ✗", state="error")
                    st.error("Max retry attempts reached. Could not execute SQL.")
                    return sql, None, None
                
                # Correct SQL
                status.update(label=f"Attempting self-correction (Attempt {attempt+1})...")
                messages = [
                    ("system", prompt),
                    ("user", f"Question: {question}"),
                    ("assistant", sql),
                    ("user", f"That query failed with database error: {db_err}\n\nPlease fix the query and return ONLY the corrected SQL query. Do not explain.")
                ]
                sql = clean_sql(model.invoke(messages).content)
                attempt += 1
                
        if results_df is None:
            return sql, None, None
            
        # Step 5: Explain Results
        status.update(label="Synthesizing plain-English explanation...")
        results_str = results_df.to_string(index=False)
        exp_prompt = EXPLANATION_PROMPT.format(
            question=question,
            sql_query=sql,
            results_str=results_str
        )
        # Higher temperature for better language synthesis
        explain_model = llm.get_llm(temperature=0.3)
        explanation = explain_model.invoke(exp_prompt).content.strip()
        
        # Mark complete
        status.update(label="Agent complete!", state="complete")
        
    return sql, results_df, explanation


# --- Database Connection Initialization ----------------------------------
@st.cache_resource
def load_db():
    """Cache connection so we don't reload Parquet files on every click."""
    return db_utils.get_db_connection()

try:
    con = load_db()
    schema = db_utils.get_database_schema(con)
except Exception as e:
    st.error(f"Error loading database files: {e}")
    st.info("Make sure you generated the database in `M3&4/Session3-SQL-DuckDB/` first by running `python generate_steering_wheel_data.py`!")
    st.stop()


# --- Sidebar UI -----------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/database.png", width=60)
    st.markdown("## Schema Inspector")
    st.markdown("Explore the registered tables and columns in real-time:")
    
    # Render table accordion views
    tables = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchall()
    for (t_name,) in tables:
        with st.expander(f"📁 {t_name}"):
            cols = con.execute(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{t_name}' ORDER BY ordinal_position").fetchall()
            for col, dtype in cols:
                st.caption(f"**{col}** ({dtype})")
                
    st.divider()
    st.markdown("### Model Configs")
    st.info(f"Model: `{llm.DEFAULT_MODEL}`")


# --- Main Header banner --------------------------------------------------
st.markdown("""
<div class="header-container">
    <div class="header-title">FactorySQL Agent</div>
    <div class="header-subtitle">Analyze steering wheel production lines using natural language. Powered by Mistral Codestral.</div>
</div>
""", unsafe_allow_html=True)


# --- Quick Prompts Selection ---------------------------------------------
st.markdown("### 💡 Quick Questions")
col1, col2, col3 = st.columns(3)

# Initialize session state for the user query if it doesn't exist
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

if col1.button("Molding station scrap rate"):
    st.session_state.user_query = "What is the scrap rate of the molding station?"
elif col2.button("Conductor resistance anomalies"):
    st.session_state.user_query = "What is the average resistance of the heating conductors?"
elif col3.button("Total yield per product type"):
    st.session_state.user_query = "Find the total count of OK vs not OK results for each product type at the quality check station"

# --- Query Interface -----------------------------------------------------
user_input = st.text_input(
    "Ask a question about the production data:",
    key="user_query",
    placeholder="e.g. What is the average cycle time at molding for premium products?"
)

if st.button("Run Agent Query", type="primary"):
    if not user_input.strip():
        st.warning("Please enter a question first.")
    else:
        # Check API Key
        try:
            llm.check_key()
        except RuntimeError as key_err:
            st.error(str(key_err))
            st.stop()
            
        # Execute Pipeline
        sql, df, explanation = run_agent_pipeline(user_input, con, schema)
        
        if df is not None:
            # 1. Show Executive Summary
            st.markdown("### 🤖 Agent Executive Summary")
            st.markdown(explanation)
            st.divider()
            
            # 2. Split layout for Data Table and SQL
            st.markdown("### 📊 Query Details & Results")
            tab1, tab2, tab3 = st.tabs(["Raw Data Table", "Generated SQL Query", "Visual Chart"])
            
            with tab1:
                st.dataframe(df, use_container_width=True)
                
            with tab2:
                st.code(sql, language="sql")
                st.caption("This SQL was generated dynamically, ran through guardrails, and executed in DuckDB.")
                
            with tab3:
                # CHALLENGE PORTION: Draw chart if possible
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                
                if len(numeric_cols) > 0:
                    x_axis = categorical_cols[0] if len(categorical_cols) > 0 else df.columns[0]
                    y_axis = numeric_cols[0]
                    
                    st.write(f"Automatically plotting **{y_axis}** against **{x_axis}**:")
                    fig = px.bar(df, x=x_axis, y=y_axis, template="plotly_dark", color_discrete_sequence=["#928dab"])
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("The returned dataset does not contain numeric fields to chart.")
                    
# =========================================================================
# YOUR CHALLENGE (30 min)
# -------------------------------------------------------------------------
# 1. Implement dynamic charts. Instead of always drawing a bar chart,
#    inspect the data shape. If there is a "timestamp" column, draw a
#    line chart showing trends over time. If there is only one numeric
#    column and no categoricals, display it as a premium KPI gauge
#    or `st.metric`.
#
# 2. Add an "Agent Trace" section inside an expander that displays
#    the query attempts and errors that the model self-corrected (from Step 04).
#    This makes the agent's invisible thinking visible to the student!
# =========================================================================
