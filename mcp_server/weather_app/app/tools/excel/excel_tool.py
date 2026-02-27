from typing import List, Dict, Optional
from app.utils.excel_service import generate_excel
from app.db.mongo import get_db
from app.server import mcp

@mcp.tool()
async def generate_excel_file(
    filename: str,
    sheet_name: str = "Sheet1",
    data: Optional[List[Dict]] = None,
    collection: Optional[str] = None,
    limit: int = 100
) -> str:
    """
    Generate an Excel file from provided data or MongoDB collection.

    Args:
        filename: Base name of Excel file.
        sheet_name: Sheet name inside Excel.
        data: List of dictionary records.
        collection: MongoDB collection name (optional).
        limit: Max records if fetching from DB.
    """

    if not data and not collection:
        return "Provide either data or collection."

    # If collection provided, fetch from Mongo
    if collection:
        db = get_db()
        cursor = db[collection].find().limit(limit)
        data = []

        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            data.append(doc)

    return await generate_excel(filename, sheet_name, data)