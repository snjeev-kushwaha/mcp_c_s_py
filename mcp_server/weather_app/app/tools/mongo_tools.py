from app.server import mcp
from app.db.mongo import get_db
from app.utils.schema import build_validator
from pymongo.errors import CollectionInvalid

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
