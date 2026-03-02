import sys
import logging

# from app.tools import alerts, forecast, mongo_tools, mongo_crud
# Import tools one by one
from app.tools.weather import alerts
from app.tools.weather import forecast
from app.tools.mongo import mongo_tools
from app.tools.mongo import mongo_crud
from app.server import mcp

def main():
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logging.error("\nMCP server stopped gracefully.")

if __name__ == "__main__":
    main()
