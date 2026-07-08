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
    representation of all registered tables, descriptions, columns, and sample rows.
    """
    import pyarrow.parquet as pq
    schema_str = []
    
    # Get all tables registered in the database
    tables = con.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'").fetchall()
    
    for (table_name,) in tables:
        schema_str.append(f"Table: {table_name}")
        
        # 1. Dynamically read metadata from Parquet schema using PyArrow
        description = "No description available"
        col_descs = {}
        
        file_name = TABLE_FILES.get(table_name)
        if file_name:
            file_path = DATA_DIR / file_name
            if file_path.exists():
                try:
                    parquet_schema = pq.read_schema(file_path)
                    if parquet_schema.metadata and b"description" in parquet_schema.metadata:
                        description = parquet_schema.metadata[b"description"].decode("utf-8")
                    
                    for field in parquet_schema:
                        if field.metadata and b"description" in field.metadata:
                            col_descs[field.name] = field.metadata[b"description"].decode("utf-8")
                except Exception:
                    pass
        
        schema_str.append(f"Description: {description}")
        schema_str.append("Columns:")
        
        # Query column information for the current table
        columns = con.execute(
            f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position"
        ).fetchall()
        
        for col_name, col_type in columns:
            col_desc = col_descs.get(col_name)
            if col_desc:
                schema_str.append(f"  - {col_name} ({col_type}): {col_desc}")
            else:
                schema_str.append(f"  - {col_name} ({col_type})")
            
        # 2. Fetch first 3 sample rows
        sample_rows = con.execute(f"SELECT * FROM {table_name} LIMIT 3").fetchall()
        if sample_rows:
            schema_str.append("Sample Rows (up to 3):")
            col_names = [col[0] for col in columns]
            for row in sample_rows:
                # Construct a clean dictionary format for the row values
                row_dict = {}
                for col, val in zip(col_names, row):
                    if val is None:
                        row_dict[col] = None
                    elif isinstance(val, (int, float)):
                        row_dict[col] = val
                    elif hasattr(val, "isoformat"):
                        row_dict[col] = val.isoformat()
                    else:
                        row_dict[col] = str(val)
                schema_str.append(f"  {row_dict}")
                
        schema_str.append("")  # empty line separator
        
    return "\n".join(schema_str)
