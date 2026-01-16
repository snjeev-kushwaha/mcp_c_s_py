import sys
import logging

# 🔴 THIS IMPORT IS REQUIRED
# from app.tools import alerts, forecast, mongo_tools, mongo_crud
# Import tools one by one
from app.tools import alerts
from app.tools import forecast
# from app.tools import mongo_tools
# from app.tools import mongo_crud

from app.server import mcp

def main():
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logging.error("\nMCP server stopped gracefully.")

if __name__ == "__main__":
    main()
