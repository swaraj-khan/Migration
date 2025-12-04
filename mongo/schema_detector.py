from typing import Any, Dict
from ..utils.flattener import flatten_document
from ..utils.logger import info



def infer_postgres_type(value: Any) -> str:
    if value is None:
        return "text"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "numeric"
    if isinstance(value, str):
        return "text"
    if hasattr(value, "isoformat"):  
        return "timestamptz"
    if isinstance(value, list):
        return "jsonb"
    return "jsonb"  


def detect_schema(doc: Dict[str, Any]) -> Dict[str, str]:
    flat = flatten_document(doc)
    schema = {}

    for key, value in flat.items():
        schema[key] = infer_postgres_type(value)

    info(f"Detected schema with {len(schema)} fields.")
    return schema
