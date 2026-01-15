from app.server import mcp
from app.db.mongo import get_db
from bson import ObjectId
import json
from app.utils.normalizer import normalize_dates, sanitize_update

ALLOWED_OPERATIONS = {"insert", "update", "delete", "find"}


@mcp.tool()
async def mongo_crud(
    operation: str,
    collection: str,
    data: dict | list[dict] | None = None,
    filter: dict | None = None,
    update: dict | None = None,
    limit: int | None = 10,
) -> str:
    """
    Perform safe CRUD operations on MongoDB.

    Args:
        operation: insert | update | delete | find
        collection: MongoDB collection name
        data: Document to insert
        filter: Filter criteria
        update: Fields to update
        limit: Max records for find
    """

    if operation not in ALLOWED_OPERATIONS:
        return f"Invalid operation: {operation}"

    db = get_db()
    col = db[collection]

    try:
        if operation == "insert":
            if not data:
                return "Insert operation requires data."
            
            # Multi insert
            if isinstance(data, list):
                if not all(isinstance(d, dict) for d in data):
                    return "All records must be objects."

                normalized = [normalize_dates(doc) for doc in data]
                result = col.insert_many(normalized)
                return {
                    "inserted_count": len(result.inserted_ids),
                    "inserted_ids": [str(_id) for _id in result.inserted_ids],
                }

            if isinstance(data, dict):
                normalized  = normalize_dates(data)
                result = col.insert_one(normalized )
                return f"Inserted document with id: {result.inserted_id}"

        elif operation == "update":
            if not filter or not update:
                return "Update operation requires filter and update."
            
            safe_update = sanitize_update(update)
            normalized_update = normalize_dates(safe_update)
            result = col.update_many(filter, {"$set": normalized_update})
            return (
                     f"Matched records: {result.matched_count}, "
                     f"Modified records: {result.modified_count}"
                 )

        elif operation == "delete":
            if not filter:
                return "Delete operation requires filter."

            result = col.delete_many(filter)
            return f"Deleted {result.deleted_count} documents."

        elif operation == "find":
            normalized_filter = normalize_dates(filter or {})
            cursor = col.find(normalized_filter).limit(limit)
            documents = []

            for doc in cursor:
                doc["_id"] = str(doc["_id"])
                documents.append(doc)

            if not documents:
                return "No records found."

            return json.dumps(documents, indent=2, default=str)

    except Exception as exc:
        return f"Database operation failed: {str(exc)}"
