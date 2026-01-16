import sys
import asyncio

from app.client import MCPClient
from app.chat import ChatLoop


async def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_mcp_server>")
        sys.exit(1)

    client = MCPClient()

    try:
        await client.connect(sys.argv[1])
        chat = ChatLoop(client)
        await chat.run()
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
