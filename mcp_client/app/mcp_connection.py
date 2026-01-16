from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class MCPConnection:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.stdio = None
        self.write = None

    async def connect(self, server_script_path: str):
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")

        if not (is_python or is_js):
            raise ValueError("Server script must be .py or .js")

        command = "python" if is_python else "node"

        params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        self.stdio, self.write = await self.exit_stack.enter_async_context(
            stdio_client(params)
        )

        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

    async def list_tools(self):
        response = await self.session.list_tools()
        return response.tools

    async def call_tool(self, name, args):
        return await self.session.call_tool(name, args)

    async def close(self):
        await self.exit_stack.aclose()
