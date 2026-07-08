"""
Step 04 — The Self-Correction Agent Loop (Retry on Error)
==========================================================

Goal:
    Even specialized models make mistakes. They might guess a column name
    incorrectly (e.g. `resistance` instead of `resistance_ohm`) or write invalid
    SQL syntax.

    Instead of crashing or giving up, an *agentic* system traps the error,
    feeds it back to the LLM along with the failing query, and asks the LLM
    to debug and correct itself.

    This loop of (Generate -> Validate -> Execute -> Catch Error -> Correct) 
    is the foundation of agentic resilience.

Run it:
    python 04_retry_loop.py
"""

import duckdb
import llm_utils as llm
import db_utils
from 03_sql_validator import validate_sql, clean_sql

SYSTEM_PROMPT = """You are a DuckDB SQL expert. Given the database schema below, write a single valid SQL query that answers the user's question.

Database Schema Context:
{schema_context}

Rules:
1. Return ONLY the raw SQL query. Do not add any conversational text.
2. Do not wrap the SQL query in markdown blocks (e.g., do not use ```sql ... ```).
3. Only use tables and columns defined in the schema.
4. Ensure the query is compatible with DuckDB SQL.
"""


def generate_sql_initial(question: str, schema_context: str) -> str:
    """Initial SQL generation attempt."""
    model = llm.get_llm(temperature=0.0)
    prompt = SYSTEM_PROMPT.format(schema_context=schema_context)
    messages = [
        ("system", prompt),
        ("user", f"Question: {question}")
    ]
    response = model.invoke(messages)
    return clean_sql(response.content)


def generate_sql_correction(question: str, schema_context: str, broken_sql: str, error_msg: str) -> str:
    """
    Sends the broken SQL and the exact database error back to the LLM,
    asking for a corrected version.
    """
    model = llm.get_llm(temperature=0.0)
    prompt = SYSTEM_PROMPT.format(schema_context=schema_context)
    
    # We build a chat history to show the LLM its mistake and the error it caused
    messages = [
        ("system", prompt),
        ("user", f"Question: {question}"),
        ("assistant", broken_sql),
        ("user", f"That query failed with the following database error:\n{error_msg}\n\nPlease correct the query and return ONLY the corrected SQL query. Do not write any explanations.")
    ]
    
    response = model.invoke(messages)
    return clean_sql(response.content)


def run_sql_agent(question: str, con: duckdb.DuckDBPyConnection, schema: str, max_attempts: int = 3):
    """
    Runs the agent loop: generates, validates, executes.
    If execution fails, it retries by sending the error back to the model.
    """
    attempt = 1
    sql = generate_sql_initial(question, schema)
    
    while attempt <= max_attempts:
        print(f"\n--- Attempt {attempt} of {max_attempts} ---")
        print(f"Generated SQL:\n{sql}")
        
        # 1. Run static validation check
        is_valid, val_error = validate_sql(sql)
        if not is_valid:
            print(f"Validator Rejected: {val_error}")
            if attempt == max_attempts:
                print("Failed to generate a valid query after maximum attempts.")
                return None
            sql = generate_sql_correction(question, schema, sql, f"Validation Error: {val_error}")
            attempt += 1
            continue
            
        # 2. Try executing the query
        try:
            results = con.execute(sql).fetchdf()
            print("\nSuccess! Results fetched:")
            return results
        except Exception as db_err:
            error_message = str(db_err)
            print(f"\nDatabase execution failed: {error_message}")
            
            if attempt == max_attempts:
                print("\nFailed to generate a correct query after maximum attempts.")
                return None
                
            # Feed the error back to the model for correction
            print("\nSending error details back to Mistral for self-correction...")
            sql = generate_sql_correction(question, schema, sql, error_message)
            attempt += 1


if __name__ == "__main__":
    con = db_utils.get_db_connection()
    schema = db_utils.get_database_schema(con)
    
    # We deliberately ask a question that is prone to naming confusion:
    # "average resistance" -> in database it's "resistance_ohm".
    # General models might generate "SELECT AVG(resistance) FROM station_conductor" first.
    # Let's see if the retry loop catches it and corrects it.
    question = "What is the average resistance of the heating conductors?"
    print(f"Goal Question: '{question}'")
    
    results = run_sql_agent(question, con, schema)
    if results is not None:
        print("\n=== Agent Final Output ===")
        print(results)
    else:
        print("\nAgent failed to resolve the query.")
        
    con.close()

# =========================================================================
# YOUR CHALLENGE (20 min)
# -------------------------------------------------------------------------
# 1. Modify the correction loop so that if the query is rejected by the 
#    validator, the agent receives the validator's specific complaint 
#    (e.g., "Access blocked: direct reads are forbidden") and corrects that
#    instead of database syntax.
#
# 2. Add an "Execution Trace Log" that records each step in a list of dicts
#    containing the attempt number, generated SQL, status (passed/failed), 
#    and the error message. Print the whole trace log at the very end
#    so the student can see the agent's thought history.
# =========================================================================
