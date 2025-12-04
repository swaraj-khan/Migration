from __future__ import annotations
from typing import Dict, Any
from .sql_client import exec_sql
from ..utils.logger import info, warn


PG_TYPE_MAP = {
    "text": "text",
    "int": "bigint",
    "float": "double precision",
    "bool": "boolean",
    "jsonb": "jsonb",
}


def _pg_quote(identifier: str) -> str:
    clean = identifier.replace('"', "").strip()
    return f'"{clean}"'


def table_exists(table: str) -> bool:
    sql = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name = %s
        );
    """
    rows = exec_sql(sql, (table,))
    return bool(rows and rows[0]["exists"])


def create_table(table: str, schema: Dict[str, str]) -> None:
    cols = []

    # built-in metadata columns
    cols.append('id uuid PRIMARY KEY DEFAULT gen_random_uuid()')
    cols.append('mongo_id text')
    cols.append('operation text')
    cols.append('timestamp timestamptz DEFAULT now()')

    # flattened fields
    for col, t in schema.items():
        pg_type = PG_TYPE_MAP.get(t, "text")
        cols.append(f'{_pg_quote(col)} {pg_type}')

    # raw JSONB
    cols.append("raw_data jsonb")

    ddl = f'CREATE TABLE "{table}" (\n  ' + ",\n  ".join(cols) + "\n);"

    exec_sql(ddl)
    info(f"Created table: {table}")



def get_existing_columns(table: str) -> Dict[str, str]:
    sql = """
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_schema='public'
          AND table_name=%s;
    """
    rows = exec_sql(sql, (table,))
    result = {}

    for row in rows:
        result[row["column_name"]] = row["data_type"]

    return result


def add_missing_columns(table: str, new_schema: Dict[str, str]) -> None:
    existing = get_existing_columns(table)

    for col, t in new_schema.items():
        if col not in existing:
            pg_type = PG_TYPE_MAP.get(t, "text")
            ddl = f'ALTER TABLE "{table}" ADD COLUMN {_pg_quote(col)} {pg_type};'
            exec_sql(ddl)
            warn(f"Added column '{col}' to table '{table}'")


def ensure_table_schema(table: str, schema: Dict[str, str]) -> None:
    if not table_exists(table):
        create_table(table, schema)
    else:
        add_missing_columns(table, schema)
