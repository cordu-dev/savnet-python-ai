"""
Session 7 — Shared Database helpers
===================================

This module connects to our DuckDB database and registers Parquet data
files from Session 3 as virtual tables. This allows our LangGraph nodes
to run live SQL queries to answer production and scrap questions.
"""

from pathlib import Path
import duckdb

# Locate the Parquet data files generated in Session 3
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "Session3-SQL-DuckDB" / "data"

TABLE_FILES = {
    "materials_stock": "materials_stock.parquet",
    "materials_log": "materials_log.parquet",
    "station_molding": "station_molding.parquet",
    "station_quality_check": "station_quality_check.parquet",
    "station_foaming": "station_foaming.parquet",
    "station_conductor": "station_conductor.parquet",
    "station_laser": "station_laser.parquet",
    "station_tapitat": "station_tapitat.parquet",
}


def get_db_connection() -> duckdb.DuckDBPyConnection:
    """Connect to an in-memory DuckDB database and register the Parquet files as views."""
    con = duckdb.connect(database=":memory:")
    
    # Verify the data directory exists
    if not DATA_DIR.exists():
        raise FileNotFoundError(
            f"\n\nData directory not found at: {DATA_DIR.resolve()}\n"
            "Please go to `M3&4/Session3-SQL-DuckDB` and run the data generator script first!"
        )

    for table_name, file_name in TABLE_FILES.items():
        file_path = DATA_DIR / file_name
        if not file_path.exists():
            raise FileNotFoundError(
                f"\n\nMissing file: {file_path.resolve()}\n"
                "Please regenerate the manufacturing data in Session 3."
            )
        
        # Register the Parquet file as a virtual view inside DuckDB
        con.execute(f"CREATE OR REPLACE VIEW {table_name} AS SELECT * FROM read_parquet('{file_path}')")
        
    return con


def run_query(query: str):
    """
    Connects to DuckDB, runs the query, and returns the results.
    Helper for LangGraph nodes.
    """
    con = get_db_connection()
    try:
        results = con.execute(query).fetchall()
        columns = [desc[0] for desc in con.description]
        return results, columns
    finally:
        con.close()


if __name__ == "__main__":
    try:
        con = get_db_connection()
        print("DuckDB database connected successfully ✓")
        print("Available tables:")
        tables = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchall()
        for (table,) in tables:
            row_count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            print(f"  - {table} ({row_count} rows)")
        con.close()
    except Exception as err:
        print(f"Database setup check failed: {err}")
