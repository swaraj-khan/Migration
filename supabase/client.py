import requests
from typing import Any, Dict
from ..config.settings import (
    SUPABASE_SERVICE_ROLE_KEY,
    SUPABASE_REST_URL,
    SUPABASE_SQL_URL,
)
from ..utils.logger import info, error



SQL_URL: str = str(SUPABASE_SQL_URL)
REST_URL: str = str(SUPABASE_REST_URL)

headers = {
    "apikey": SUPABASE_SERVICE_ROLE_KEY,
    "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
    "Content-Type": "application/json",
}


def execute_sql(sql: str) -> Dict[str, Any]:

    payload = {"query": sql}

    try:
        resp = requests.post(SQL_URL, headers=headers, json=payload)

        if resp.status_code >= 400:
            error(f"SQL Error [{resp.status_code}]: {resp.text}\nSQL: {sql}")
            raise Exception(resp.text)

        return resp.json()

    except Exception as e:
        error(f"Failed to execute SQL: {e}")
        raise


def rest_insert(table: str, row: Dict[str, Any]) -> None:

    url = f"{REST_URL}/{table}"

    try:
        resp = requests.post(url, headers=headers, json=row)

        if resp.status_code >= 400:
            error(f"REST Insert Error [{resp.status_code}]: {resp.text}")
            raise Exception(resp.text)

    except Exception as e:
        error(f"Failed to insert row: {e}")
        raise

    info(f"Inserted into {table}")
