from openpyxl import Workbook
from typing import List, Dict
import os
import datetime

EXPORT_DIR = "exports"
os.makedirs(EXPORT_DIR, exist_ok=True)


async def generate_excel(
    filename: str,
    sheet_name: str,
    data: List[Dict]
) -> str:
    wb = Workbook()
    ws = wb.active
    ws.title = sheet_name

    if not data:
        return "No data provided."

    # Write headers
    headers = list(data[0].keys())
    ws.append(headers)

    # Write rows
    for row in data:
        ws.append([row.get(col) for col in headers])

    # Timestamp filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(EXPORT_DIR, f"{filename}_{timestamp}.xlsx")

    wb.save(file_path)

    return file_path