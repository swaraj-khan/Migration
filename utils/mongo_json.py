from bson import ObjectId
from datetime import datetime, date, time
from decimal import Decimal
from typing import Any, Dict, List


def convert_mongo_types(value: Any) -> Any:
    """Recursively convert MongoDB/Python types into JSON-safe types."""

    # MongoDB ObjectId
    if isinstance(value, ObjectId):
        return str(value)

    # Datetime → ISO string
    if isinstance(value, datetime):
        return value.isoformat()

    # Date → ISO (YYYY-MM-DD)
    if isinstance(value, date):
        return value.isoformat()

    # Time → HH:MM:SS
    if isinstance(value, time):
        return value.isoformat()

    # Decimal / BSON Decimal128
    if isinstance(value, Decimal):
        return float(value)

    # Dict → recursive
    if isinstance(value, dict):
        return {k: convert_mongo_types(v) for k, v in value.items()}

    # List → recursive
    if isinstance(value, list):
        return [convert_mongo_types(v) for v in value]

    return value
