from __future__ import annotations
from typing import Any, Dict, List, cast
from pathlib import Path
from bson import json_util
from pymongo.collection import Collection
from pymongo.errors import PyMongoError
from ..supabase.table_manager import ensure_table_schema
from ..supabase.inserter import insert_row
from .client import get_db
from .schema_detector import detect_schema
from ..utils.logger import info, warn, error



RESUME_FILE = Path(__file__).resolve().parents[1] / "state" / "resume_tokens.json"


def load_resume_tokens() -> Dict[str, Any]:
    if not RESUME_FILE.exists():
        return {}

    content = RESUME_FILE.read_text(encoding="utf-8").strip()
    if not content:
        return {}

    data = json_util.loads(content)
    if isinstance(data, dict):
        return cast(Dict[str, Any], data)
    return {}


def save_resume_tokens(tokens: Dict[str, Any]) -> None:
    serialized = json_util.dumps(tokens)
    RESUME_FILE.write_text(serialized, encoding="utf-8")


def process_change(collection: Collection, coll_name: str, change: Dict[str, Any]) -> None:
    op_type = change.get("operationType")

    doc_key = change.get("documentKey", {})
    doc_id = doc_key.get("_id")

    if op_type == "insert":
        operation = "CREATE"
    elif op_type in ("update", "replace"):
        operation = "UPDATE"
    elif op_type == "delete":
        operation = "DELETE"
    else:
        warn(f"Ignoring unsupported operationType: {op_type}")
        return

    if op_type == "delete":
        doc: Dict[str, Any] = {"_id": doc_id}
    else:
        doc_found = collection.find_one({"_id": doc_id})
        if not doc_found:
            warn(f"Document with _id={doc_id} not found for operation {op_type}")
            return
        doc = cast(Dict[str, Any], doc_found)

    schema = detect_schema(doc)

    ensure_table_schema(coll_name, schema)

    insert_row(coll_name, doc, operation, schema)



# def watch_collection(collection_name: str) -> None:
#     db = get_db()
#     collection: Collection = db[collection_name]

#     tokens = load_resume_tokens()
#     resume_token = tokens.get(collection_name)

#     info(f"Starting change stream for collection '{collection_name}'")

#     while True:
#         try:
#             if resume_token is not None:
#                 change_stream = collection.watch(resume_after=resume_token)
#             else:
#                 change_stream = collection.watch()

#             for change in change_stream:
#                 process_change(collection, collection_name, cast(Dict[str, Any], change))

#                 resume_token = change.get("_id")
#                 tokens[collection_name] = resume_token
#                 save_resume_tokens(tokens)

#         except PyMongoError as e:
#             error(f"Change stream error on '{collection_name}': {e}")
#             warn("Retrying change stream after error...")
#             continue
#         except KeyboardInterrupt:
#             info("Change stream interrupted by user.")
#             break


def watch_collection(collection, coll_name: str):
    info(f"[{coll_name}] Starting change stream")

    try:
        with collection.watch() as stream:
            for change in stream:
                process_change(collection, coll_name, change)
    except Exception as e:
        error(f"[{coll_name}] Fatal error: {e}")
