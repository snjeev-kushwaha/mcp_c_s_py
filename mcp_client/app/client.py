from app.mcp_connection import MCPConnection

# from app.openai_client import OpenAIClient
from app.ollama_client import OllamaClient


class MCPClient:
    def __init__(self):
        self.mcp = MCPConnection()
        # self.llm = OpenAIClient()
        self.llm = OllamaClient()

    async def connect(self, server_path: str):
        await self.mcp.connect(server_path)
        tools = await self.mcp.list_tools()
        print("\nConnected with tools:", [t.name for t in tools])

    async def process_query(self, query: str) -> str:
        # messages = [{"role": "user", "content": query}]
        messages = [
                     {
                         "role": "system",
                         "content": (
                             "You are an AI assistant that MUST use tools when relevant. "
                             "If the user asks about weather, you MUST call the weather tool. "
                             "Do not explain limitations. Do not refuse. "
                             "If required parameters are missing, infer them."
                         )
                     },
                     {
                         "role": "user",
                         "content": query
                     }
                   ]

        tools = await self.mcp.list_tools()
        available_tools = [
            {
                "type": "function",
                "function": {
                    "name": t.name,
                    "description": t.description,
                    "parameters": t.inputSchema,
                },
            }
            for t in tools
        ]

        response = self.llm.create_message(messages, available_tools)

        final_text = []

        msg = response["message"]

        if msg.get("content"):
            final_text.append(msg["content"])

        if "tool_calls" in msg:
            for call in msg["tool_calls"]:
                fn = call["function"]
                tool_name = fn["name"]
                tool_args = fn.get("arguments", {})

                result = await self.mcp.call_tool(tool_name, tool_args)

                messages.append(
                    {"role": "tool", "name": tool_name, "content": str(result.content)}
                )

            followup = self.llm.create_message(messages)
            final_text.append(followup["message"]["content"])

        return "\n".join(final_text)

    async def close(self):
        await self.mcp.close()
