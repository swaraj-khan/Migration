from __future__ import annotations

from typing import Dict, Any, List
from psycopg2.extras import Json

from .sql_client import exec_sql
from ..utils.flattener import flatten_document
from ..utils.logger import info
from ..utils.mongo_json import convert_mongo_types


def _pg_quote(identifier: str) -> str:
    """Safely quote PostgreSQL identifiers (remove accidental inner quotes)."""
    clean = identifier.replace('"', "").strip()
    return f'"{clean}"'



def build_row(doc: Dict[str, Any], operation: str) -> Dict[str, Any]:
    """
    Build a final row for insertion into Postgres.
    """

    # Convert ALL MongoDB native types first
    safe_doc = convert_mongo_types(doc)

    mongo_id = safe_doc.get("_id")
    flat = flatten_document(safe_doc)

    row: Dict[str, Any] = {
        "mongo_id": str(mongo_id) if mongo_id else None,
        "operation": operation,
        "raw_data": Json(safe_doc),  # Now JSON-serializable
    }

    row.update(flat)
    return row

def insert_row(table: str, doc: Dict[str, Any], operation: str, schema: Dict[str, str]) -> None:
    row = build_row(doc, operation)

    columns = list(row.keys())
    cols_sql = ", ".join(_pg_quote(c) for c in columns)
    placeholders = ", ".join(["%s"] * len(columns))

    sql = f'INSERT INTO "{table}" ({cols_sql}) VALUES ({placeholders});'

    safe_values = []

    for col, val in row.items():

        # If schema says jsonb, ALWAYS wrap value as Json
        if schema.get(col) == "jsonb":
            safe_values.append(Json(val))
            continue

        # dict / list must also be Json()
        if isinstance(val, (dict, list)):
            safe_values.append(Json(val))
            continue

        safe_values.append(val)

    exec_sql(sql, safe_values)
    info(f"Replicated {operation} -> {table}")

