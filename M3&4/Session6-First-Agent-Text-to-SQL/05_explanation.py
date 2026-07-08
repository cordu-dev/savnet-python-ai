"""
Step 05 — Generating Plain-English Explanations
================================================

Goal:
    Raw tables and numbers are not friendly to business users. A factory manager
    asking a question doesn't want to read a pandas DataFrame or understand a 
    complex inner join. They want a direct answer in plain English.

    In this script, we add a final step:
        1. Run the Text-to-SQL agent to get the results.
        2. Feed the user's question, the executed SQL, and the query results
           back into Mistral.
        3. Prompt the model to write a clear, executive summary explaining
           *what* the query found and *what* it means.

Run it:
    python 05_explanation.py
"""

import re
import pandas as pd
import llm_utils as llm
import db_utils

# --- 1. Prompts ----------------------------------------------------------
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
3. Point out any interesting findings (e.g. high values, trends, anomalies).
4. List any critical caveats (e.g. "This only counts sport and premium models since standard models do not have heating wires").
5. Keep it professional, structured, and easy to read.
"""


def clean_sql(raw_sql: str) -> str:
    """Extracts raw SQL from markdown blocks if the LLM wraps it."""
    match = re.search(r"```sql\s+(.*?)\s*```", raw_sql, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    match = re.search(r"```\s+(.*?)\s*```", raw_sql, re.DOTALL)
    if match:
        return match.group(1).strip()
    return raw_sql.strip()


def generate_sql(question: str, schema_context: str) -> str:
    """Send the schema and question to Mistral and return the SQL query."""
    model = llm.get_llm(temperature=0.0)
    prompt = SQL_PROMPT.format(schema_context=schema_context)
    messages = [
        ("system", prompt),
        ("user", f"Question: {question}")
    ]
    response = model.invoke(messages)
    return clean_sql(response.content)


def explain_results(question: str, sql_query: str, df_results: pd.DataFrame) -> str:
    """Sends the context to Mistral and returns a plain-English explanation."""
    model = llm.get_llm(temperature=0.3)  # Slightly higher temp for natural language writing
    
    # Convert DataFrame to a clean string format
    results_str = df_results.to_string(index=False)
    
    prompt = EXPLANATION_PROMPT.format(
        question=question,
        sql_query=sql_query,
        results_str=results_str
    )
    
    response = model.invoke(prompt)
    return response.content.strip()


if __name__ == "__main__":
    con = db_utils.get_db_connection()
    schema = db_utils.get_database_schema(con)
    
    # Define a complex business question
    question = "Which operator has the highest scrap rate at the molding station, and how many units did they scrap?"
    print(f"User Question: '{question}'\n")
    
    print("Agent: Generating SQL query...")
    sql_query = generate_sql(question, schema)
    print(f"SQL Generated: {sql_query}\n")
    
    try:
        results_df = con.execute(sql_query).fetchdf()
        print("Agent: Query succeeded. Fetching analysis...")
        
        # Generate explanation
        explanation = explain_results(question, sql_query, results_df)
        
        print("\n=== FINAL AGENT RESPONSE ===")
        print(explanation)
        print("============================\n")
    except Exception as e:
        print(f"Execution error: {e}")
        
    con.close()

# =========================================================================
# YOUR CHALLENGE (15 min)
# -------------------------------------------------------------------------
# 1. Modify the prompt to enforce a structured Markdown report format. 
#    The output must contain three specific headers: 
#    - **Executive Summary**
#    - **How the Data Was Calculated**
#    - **Observations & Caveats**
#
# 2. What happens if the query returns an empty DataFrame?
#    Add a check in the script: if the DataFrame is empty, feed it to a 
#    special prompt asking Mistral to explain why there might be no records
#    for the user's question (e.g. testing with "List all standard wheels that
#    failed the laser station" — remember PT55 standard wheels don't go to 
#    the laser station!).
# =========================================================================
