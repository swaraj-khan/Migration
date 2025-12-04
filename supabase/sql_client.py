import psycopg2
import psycopg2.extras
from ..config.settings import (
    PG_USER,
    PG_PASSWORD,
    PG_HOST,
    PG_PORT,
    PG_DATABASE,
)
from ..utils.logger import info, error

_connection = None


def get_conn():
    global _connection
    if _connection is None:
        try:
            _connection = psycopg2.connect(
                user=PG_USER,
                password=PG_PASSWORD,
                host=PG_HOST,
                port=PG_PORT,
                database=PG_DATABASE,
            )
            info("Connected to Supabase Postgres (Session Pooler)")
        except Exception as e:
            error(f"Failed to connect to Supabase Postgres: {e}")
            raise

    return _connection


def exec_sql(sql: str, params=None):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cur.execute(sql, params)
        try:
            rows = cur.fetchall()
        except psycopg2.ProgrammingError:
            rows = []

        conn.commit()
        return rows
    except Exception as e:
        error(f"SQL execution failed: {e}\nSQL: {sql}")
        conn.rollback()
        raise
