from mcp.server.fastmcp import FastMCP
import sys

mcp = FastMCP("test")

@mcp.tool()
async def ping() -> str:
    return "pong"

def main():
    sys.stderr.write("SERVER READY\n")
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()
