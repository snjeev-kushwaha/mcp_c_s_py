from app.server import mcp
from app.db.mongo import get_db
from app.utils.schema import build_validator, infer_type
from pymongo.errors import CollectionInvalid
from collections import defaultdict

@mcp.tool()
async def create_collection(
    collection_name: str,
    fields: dict[str, str]
) -> str:
    """
    Create a MongoDB collection dynamically with schema validation.

    Args:
        collection_name: Name of the collection to create
        fields: Field definitions (e.g. {"name": "string", "age": "number"})
    """
    db = get_db()

    if not collection_name.isidentifier():
        return "Invalid collection name."

    try:
        validator = build_validator(fields)

        db.create_collection(
            collection_name,
            validator=validator
        )

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
    Inspect MongoDB and return inferred schema for all collections.

    Args:
        sample_size: Number of documents to sample per collection
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
            "fields": {
                field: list(types)
                for field, types in fields.items()
            }
        }

    return schema