from app.server import mcp
from app.db.mongo import get_db
from app.utils.schema import build_validator, infer_type
from pymongo.errors import CollectionInvalid
from collections import defaultdict


@mcp.tool()
async def create_collection(collection_name: str, fields: dict[str, str]) -> str:
    """
    Create a MongoDB collection dynamically with schema validation.

    Args:
        collection_name: Name of the MongoDB collection.
        fields: Field definitions with type mapping, e.g., {"name": "string", "age": "number"}.
    """
    try:
        db = get_db()
    except Exception as e:
        return f"Mongo connection failed: {str(e)}"

    if not collection_name.isidentifier():
        return "Invalid collection name."

    try:
        validator = build_validator(fields)

        db.create_collection(collection_name, validator=validator)

        return (
            f"Collection '{collection_name}' created successfully.\n"
            f"Fields: {', '.join(fields.keys())}"
        )

    except CollectionInvalid:
        return f"Collection '{collection_name}' already exists."

    except Exception as exc:
        return f"Failed to create collection: {str(exc)}"


@mcp.tool()
async def get_db_schema(sample_size: int = 20) -> dict:
    """
    Return MongoDB collections and inferred schema.

    Args:
        sample_size: Number of documents to sample from each collection (default 20).
    """
    db = get_db()
    schema = {}

    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        fields = defaultdict(set)

        cursor = collection.find({}, limit=sample_size)

        for doc in cursor:
            for key, value in doc.items():
                fields[key].add(infer_type(value))

        schema[collection_name] = {
            "fields": {field: list(types) for field, types in fields.items()}
        }

    return schema

@mcp.tool()
async def get_total_collections() -> int:
    """
    Return the total number of collections (tables) in the MongoDB database.
    """
    db = get_db()
    return len(db.list_collection_names())