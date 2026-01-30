# agent/memory.py

class Memory:
    def __init__(self):
        self.logs = []

    def add(self, entry: str):
        self.logs.append(entry)

    def get_all(self):
        return self.logs
