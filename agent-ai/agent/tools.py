# agent/tools.py

def search(query: str) -> str:
    return f"Search result for '{query}'"

def calculate(expression: str) -> str:
    try:
        return str(eval(expression))
    except Exception:
        return "Calculation error"
