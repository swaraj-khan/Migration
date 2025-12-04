import os
from dotenv import load_dotenv

load_dotenv()

PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_HOST = os.getenv("PG_HOST")

_pg_port = os.getenv("PG_PORT")
PG_PORT = int(_pg_port) if _pg_port is not None else 5432

PG_DATABASE = os.getenv("PG_DATABASE")


REQUIRED_VARS = [
    "MONGO_URI",
    "MONGO_DB",
    "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY",
    "SUPABASE_REST_URL",
    "SUPABASE_SQL_URL",
    
]

missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
if missing:
    raise ValueError(f"❌ Missing required env variables: {', '.join(missing)}")

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

SUPABASE_REST_URL = os.getenv("SUPABASE_REST_URL")   
SUPABASE_SQL_URL = os.getenv("SUPABASE_SQL_URL")     
SUPABASE_RPC_URL = os.getenv("SUPABASE_RPC_URL")     

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
BATCH_SIZE = int(os.getenv("BATCH_SIZE", "1"))

assert MONGO_URI is not None
assert MONGO_DB is not None

assert SUPABASE_URL is not None
assert SUPABASE_SERVICE_ROLE_KEY is not None
assert SUPABASE_REST_URL is not None
assert SUPABASE_SQL_URL is not None
