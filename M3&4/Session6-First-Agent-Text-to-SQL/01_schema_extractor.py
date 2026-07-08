"""
Step 01 — Database Schema Extractor (LLM Context Prep)
======================================================

Goal:
    In order for a Text-to-SQL agent to write correct queries, it must know:
        1. What tables exist in the database.
        2. What columns are in each table.
        3. The data type of each column.

    We will use DuckDB to read the Parquet data files generated in Session 3,
    query DuckDB's catalog schema, and output a clean "schema string" ready 
    to be injected into our LLM prompt.

    To keep our code clean, we import our database helpers from `db_utils.py`.

Run it:
    python 01_schema_extractor.py
"""

import db_utils

if __name__ == "__main__":
    print("Connecting to DuckDB and loading Parquet data...")
    try:
        connection = db_utils.get_db_connection()
        print("Data loaded successfully!")
        
        print("\n=== Generating Database Schema Context ===\n")
        schema_context = db_utils.get_database_schema(connection)
        print(schema_context)
        
        # Close connection
        connection.close()
    except Exception as err:
        print(f"Error: {err}")

# =========================================================================
# YOUR CHALLENGE (15 min)
# -------------------------------------------------------------------------
# 1. Modify the `get_database_schema` function in `db_utils.py` to include
#    sample data. For each table, fetch the first 3 rows
#    (`SELECT * FROM table LIMIT 3`) and append them to the schema description.
#    Why is having sample rows useful for an LLM generating SQL?
#
# 2. Add table metadata descriptions. In `db_utils.py`, create a dictionary
#    that maps table names to a short description (e.g. 
#    `{"station_molding": "Molding station parameters for Mg skeleton injection"}`). 
#    Inject these descriptions into the output schema context.
# =========================================================================
#
# CHALLENGE SOLUTION & ANALYSIS:
# -------------------------------------------------------------------------
# We resolved the challenge by updating `db_utils.py` and the data generator:
#
# 1. Table & Column Descriptions: Instead of hardcoding descriptions in a dictionary,
#    we embedded descriptions for both the tables and all individual columns directly
#    into the Parquet schema footers using PyArrow metadata during generation.
#    `get_database_schema` in `db_utils.py` dynamically extracts this metadata using 
#    `pyarrow.parquet.read_schema(file_path)` and prints column-level documentation.
#
# 2. Sample Row Injection: Added a query (`SELECT * FROM table LIMIT 3`)
#    inside `get_database_schema` to retrieve 3 sample rows. Each row is 
#    formatted as a dictionary mapping column names to values, converting 
#    non-standard types like datetime into strings.
#
# Why having sample rows is useful for the LLM:
# - Disambiguates categorical values: Shows if a success flag is 'OK', 'PASS', or 1.
# - Shows formats & schemas: Illustrates datetime/timestamp formats and ID styles
#   (e.g., 'PID000001' vs 'P-1') which helps the LLM write correct joins and filters.
# - Reveals Units: Demonstrates physical measurement units (e.g. 'weight_g' values).
# =========================================================================

