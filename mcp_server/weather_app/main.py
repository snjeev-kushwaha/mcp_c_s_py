import sys
import logging

# 🔴 THIS IMPORT IS REQUIRED
from app.tools import alerts, forecast, mongo_tools, mongo_crud

from app.server import mcp

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr
)

def main():
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        print("\nMCP server stopped gracefully.")

if __name__ == "__main__":
    main()
