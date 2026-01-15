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
