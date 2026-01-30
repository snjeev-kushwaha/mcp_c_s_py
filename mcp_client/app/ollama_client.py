import ollama

class OllamaClient:
    def __init__(self):
        self.model = "llama3.1:8b"

    def create_message(self, messages, tools=None):
        response = ollama.chat(
            model=self.model,
            messages=messages,
            tools=tools
        )
        return response
