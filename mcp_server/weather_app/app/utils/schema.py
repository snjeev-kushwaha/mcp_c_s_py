from bson import ObjectId
import datetime

def mongo_type(field_type: str) -> dict:
    mapping = {
        "string": {"bsonType": "string"},
        "number": {"bsonType": ["int", "double"]},
        "boolean": {"bsonType": "bool"},
        "date": {"bsonType": "date"},
        "object": {"bsonType": "object"},
        "array": {"bsonType": "array"},
    }
    return mapping.get(field_type.lower(), {"bsonType": "string"})


def build_validator(fields: dict) -> dict:
    properties = {}

    for name, ftype in fields.items():
        properties[name] = mongo_type(ftype)

    return {
        "$jsonSchema": {
            "bsonType": "object",
            "required": list(fields.keys()),
            "properties": properties,
        }
    }

def infer_type(value):
    if isinstance(value, str):
        return "string"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if isinstance(value, datetime.datetime):
        return "date"
    if isinstance(value, ObjectId):
        return "objectId"
    return "unknown"