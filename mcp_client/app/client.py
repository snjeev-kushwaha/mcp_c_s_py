import json
from app.middleware.normalizer import normalize_mongo_args
from app.mcp_connection import MCPConnection
from app.ollama_client import OllamaClient
from app.tool_router import detect_domain, filter_tools
from app.prompts import build_system_prompt
from app.utils import normalize_tool_args


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
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an MCP client.\n"
                    "Rules:\n"
                    "1. You MUST use real MCP tool_calls.\n"
                    "2. Do NOT describe tool calls in text.\n"
                    "3. For database queries, always call mongo_crud.\n"
                    "4. mongo_crud.filter MUST be an object.\n"
                    "5. mongo_crud.limit MUST be an integer.\n"
                    "6. Do not answer without executing tools.\n"
                ),
            },
            {"role": "user", "content": query},
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

        if not msg.get("tool_calls"):
            return (
                "The model did not execute any tool.\n"
                "This usually means the LLM failed to emit proper MCP tool calls.\n"
                "Please retry."
            )

        if "tool_calls" in msg:
            for call in msg["tool_calls"]:
                fn = call["function"]
                tool_name = fn["name"]
                # tool_args = fn.get("arguments", {})
                # if tool_name == "mongo_crud":
                tool_args = normalize_mongo_args(fn.get("arguments", {}))
                if isinstance(tool_args.get("data"), str):
                    try:
                        tool_args["data"] = json.loads(tool_args["data"])
                    except json.JSONDecodeError:
                        tool_args["data"] = {}

                result = await self.mcp.call_tool(tool_name, tool_args)

                messages.append(
                    {"role": "tool", "name": tool_name, "content": str(result.content)}
                )

            followup = self.llm.create_message(messages, available_tools)
            final_text.append(followup["message"]["content"])

        return "\n".join(final_text)

    # async def process_query(self, query: str) -> str:
    #     domain = detect_domain(query)
    #     system_prompt = build_system_prompt(domain)

    #     messages = [
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": query},
    #     ]

    #     all_tools = await self.mcp.list_tools()
    #     selected_tools = filter_tools(all_tools, domain)

    #     available_tools = [
    #         {
    #             "type": "function",
    #             "function": {
    #                 "name": t.name,
    #                 "description": t.description,
    #                 "parameters": t.inputSchema,
    #             },
    #         }
    #         for t in selected_tools
    #     ]

    #     response = self.llm.create_message(messages, available_tools)
    #     msg = response["message"]
    #     final_text = []

    #     if msg.get("content"):
    #         final_text.append(msg["content"])

    #     if "tool_calls" in msg:
    #         for call in msg["tool_calls"]:
    #             fn = call["function"]
    #             tool_name = fn["name"]
    #             tool_args = normalize_tool_args(fn.get("arguments", {}))

    #             result = await self.mcp.call_tool(tool_name, tool_args)

    #             messages.append(
    #                 {"role": "tool", "name": tool_name, "content": str(result.content)}
    #             )

    #         followup = self.llm.create_message(messages, available_tools)
    #         final_text.append(followup["message"]["content"])

    #     return "\n".join(final_text)

    async def close(self):
        await self.mcp.close()
