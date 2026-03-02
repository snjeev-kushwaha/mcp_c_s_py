from datetime import datetime
from typing import Any

def normalize_dates(document: dict) -> dict:
    normalized = {}

    for key, value in document.items():
        if isinstance(value, str):
            try:
                normalized[key] = datetime.fromisoformat(value)
            except ValueError:
                normalized[key] = value

        elif isinstance(value, dict):
            normalized[key] = normalize_dates(value)

        elif isinstance(value, list):
            normalized[key] = [
                normalize_dates(v) if isinstance(v, dict) else v
                for v in value
            ]

        else:
            normalized[key] = value

    return normalized

def validate_documents(data, schema_fields):
    for doc in data:
        for field in schema_fields:
            if field not in doc:
                return False
    return True

def sanitize_update(update: dict) -> dict:
    # If Claude already sent $set, unwrap it
    if "$set" in update and isinstance(update["$set"], dict):
        return update["$set"]
    return update