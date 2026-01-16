from app.mcp_connection import MCPConnection
from app.openai_client import OpenAIClient


class MCPClient:
    def __init__(self):
        self.mcp = MCPConnection()
        self.llm = OpenAIClient()

    async def connect(self, server_path: str):
        await self.mcp.connect(server_path)
        tools = await self.mcp.list_tools()
        print("\nConnected with tools:", [t.name for t in tools])

    async def process_query(self, query: str) -> str:
        messages = [{"role": "user", "content": query}]

        tools = await self.mcp.list_tools()
        available_tools = [{
            "type": "function",
            "function": {
                "name": t.name,
                "description": t.description,
                "parameters": t.inputSchema
            }
        } for t in tools]

        response = self.llm.create_message(messages, available_tools)

        final_text = []

        msg = response.choices[0].message

        if msg.content:
            final_text.append(msg.content)

        if msg.tool_calls:
            for call in msg.tool_calls:
                tool_name = call.function.name
                tool_args = eval(call.function.arguments)

                result = await self.mcp.call_tool(tool_name, tool_args)

                messages.append(msg)
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": str(result.content)
                })

                followup = self.llm.create_message(messages, available_tools)
                final_text.append(followup.choices[0].message.content)

        return "\n".join(final_text)

    async def close(self):
        await self.mcp.close()
