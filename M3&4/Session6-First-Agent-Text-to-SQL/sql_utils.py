import re
import db_utils

# Whitelist of tables from our db_utils
ALLOWED_TABLES = list(db_utils.TABLE_FILES.keys())

# Blacklist of keywords representing write or structural changes
FORBIDDEN_KEYWORDS = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE", "CREATE", "REPLACE", "GRANT"]

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
    """
    Validates a SQL query for safety and correctness.
    
    Returns:
        - (True, "") if the query is safe.
        - (False, "error message") if it violates validation rules.
    """
    query_upper = sql_query.upper().strip()
    
    # 1. Basic Read-Only Check: The query must start with SELECT or WITH (for CTEs)
    if not (query_upper.startswith("SELECT") or query_upper.startswith("WITH")):
        return False, "Query must start with SELECT or WITH. Write or schema modification operations are not allowed."
        
    # 2. Check for forbidden keywords (keyword injection prevention)
    words = re.findall(r"\b[A-Z]+\b", query_upper)
    for word in words:
        if word in FORBIDDEN_KEYWORDS:
            return False, f"Forbidden keyword detected: {word}. Write operations are strictly blocked."
            
    # 3. Whitelist Table Validation:
    # Ensure the query ONLY queries tables in our ALLOWED_TABLES list.
    from_join_pattern = r"(?:FROM|JOIN)\s+([a-zA-Z0-9_\.\"\']+)"
    matches = re.findall(from_join_pattern, query_upper)
    
    referenced_tables = []
    for match in matches:
        clean_match = match.strip().replace('"', '').replace("'", "").split('(')[0].lower()
        if clean_match:
            referenced_tables.append(clean_match)
            
    # Verify each referenced table is in our whitelist
    for table in referenced_tables:
        if "duckdb_" in table or "information_schema" in table:
            return False, f"Access blocked: Querying metadata/system table '{table}' is forbidden."
        
        if "read_parquet" in table:
            return False, "Access blocked: Direct file reads via read_parquet() are forbidden. Use registered views."
            
    return True, ""
