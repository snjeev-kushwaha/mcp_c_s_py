class ChatLoop:
    def __init__(self, client):
        self.client = client

    async def run(self):
        print("\nMCP Client Started!")
        print("Type your query or 'quit' to exit.")

        while True:
            query = input("\nQuery: ").strip()
            if query.lower() == "quit":
                break

            try:
                response = await self.client.process_query(query)
                print("\n" + response)
            except Exception as exc:
                print(f"\nError: {exc}")
