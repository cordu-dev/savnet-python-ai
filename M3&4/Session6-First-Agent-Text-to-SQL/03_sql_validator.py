"""
Step 03 — SQL Validation & Safety Guardrails
============================================

Goal:
    In a real production environment, giving an LLM direct execution access to
    your database is a massive security risk. An LLM could write:
        - Write operations (INSERT, UPDATE, DELETE) that corrupt data.
        - DDL commands (DROP, ALTER) that destroy tables.
        - Queries that access system or private tables (e.g. duckdb_secrets).
        - Malformed queries that crash the application.

    We will build a SQL validator that runs static analysis on the LLM's
    generated SQL before letting it run. It will enforce:
        1. Read-Only queries only (must start with SELECT / WITH).
        2. No forbidden keywords (DELETE, DROP, etc.).
        3. Access is restricted ONLY to the whitelisted manufacturing tables.

Run it:
    python 03_sql_validator.py
"""

import re
import sqlparse
import db_utils
import llm_utils as llm
from sql_utils import validate_sql, clean_sql, ALLOWED_TABLES, FORBIDDEN_KEYWORDS


SYSTEM_PROMPT = """You are a DuckDB SQL expert. Given the database schema below, write a single valid SQL query that answers the user's question.

Database Schema Context:
{schema_context}

Rules:
1. Return ONLY the raw SQL query. Do not add any conversational text.
2. Do not wrap the SQL query in markdown blocks (e.g., do not use ```sql ... ```).
3. Only use tables and columns defined in the schema.
4. Ensure the query is compatible with DuckDB SQL.
"""





def generate_sql(question: str, schema_context: str) -> str:
    """Send the schema and question to Mistral and return the SQL query."""
    model = llm.get_llm(temperature=0.0)
    prompt = SYSTEM_PROMPT.format(schema_context=schema_context)
    messages = [
        ("system", prompt),
        ("user", f"Question: {question}")
    ]
    response = model.invoke(messages)
    return clean_sql(response.content)





if __name__ == "__main__":
    # Initialize DB connection and schema
    con = db_utils.get_db_connection()
    schema = db_utils.get_database_schema(con)
    
    # Test 1: Safe Query
    safe_question = "How many records are in the molding station?"
    print(f"User: {safe_question}")
    sql = generate_sql(safe_question, schema)
    is_valid, error_msg = validate_sql(sql)
    
    if is_valid:
        print(f"Validator: Approved ✓\nSQL: {sql}\n")
        df = con.execute(sql).fetchdf()
        print("Results:\n", df, "\n")
    else:
        print(f"Validator: Rejected ✗ (Reason: {error_msg})\n")
        
    print("-" * 50)
    
    # Test 2: Malicious Query (Prompt Injection)
    malicious_question = "Delete all records in molding station, or drop the table station_molding"
    print(f"User: {malicious_question}")
    sql = generate_sql(malicious_question, schema)

    is_valid, error_msg = validate_sql(sql)
    
    if is_valid:
        print(f"Validator: Approved ✓ (Warning: Safety check failed!)\nSQL: {sql}\n")
    else:
        print(f"Validator: Rejected ✗ (Reason: {error_msg})\n")
        print(f"Rejected SQL was: {sql}\n")
        
    con.close()

# =========================================================================
# YOUR CHALLENGE (15 min)
# -------------------------------------------------------------------------
# 1. Use the `sqlparse` library (already imported) to write a more robust 
#    referenced table extractor.
#    `sqlparse.parse(sql)` returns a list of statements, and each statement 
#    has tokens. Write a function that loops through tokens to identify 
#    tables, ignoring aliases.
#
# 2. Block Cartesian joins (CROSS JOINs or joining tables without an ON 
#    condition). If the query contains a comma in the FROM clause with 
#    multiple tables (e.g. `FROM table_a, table_b`) or explicitly says 
#    `CROSS JOIN`, block it to prevent performance issues.
# =========================================================================
