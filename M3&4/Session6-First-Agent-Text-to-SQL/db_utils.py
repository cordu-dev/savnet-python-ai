"""
Session 6 — Shared Database helpers
===================================

This is the ONE place where we set up the connection to our DuckDB database and
retrieve the schema metadata. By centralizing this, we avoid duplicate code
across all lab steps.
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
    
    # Verify the data files exist
    if not DATA_DIR.exists():
        raise FileNotFoundError(
            f"\n\nData directory not found at: {DATA_DIR.resolve()}\n"
            "Please go to `M3&4/Session3-SQL-DuckDB` and run:\n"
            "  python generate_steering_wheel_data.py\n"
            "to create the dataset first!"
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


def get_database_schema(con: duckdb.DuckDBPyConnection) -> str:
    """
    Query the DuckDB information schema and build a clean, readable text
    representation of all registered tables and columns.
    """
    schema_str = []
    
    # Get all tables registered in the database
    tables = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchall()
    
    for (table_name,) in tables:
        schema_str.append(f"Table: {table_name}")
        schema_str.append("Columns:")
        
        # Query column information for the current table
        columns = con.execute(
            f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position"
        ).fetchall()
        
        for col_name, col_type in columns:
            schema_str.append(f"  - {col_name} ({col_type})")
            
        schema_str.append("")  # empty line separator
        
    return "\n".join(schema_str)
