# agent/observer.py

class Observer:
    def observe(self, step: str, result: str):
        if "error" in result.lower():
            return "❌ Failed"
        return "✅ Success"
