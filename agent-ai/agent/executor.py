# # agent/executor.py

# from agent.prompts import load_prompt
# from agent import tools

# class Executor:
#     def execute(self, step: str):
#         prompt = load_prompt("executor")
#         prompt = prompt.replace("{step}", step)

#         print("\n⚙️ EXECUTOR PROMPT:\n", prompt)

#         if "Search" in step:
#             return tools.search(step)

#         return "Execution completed"

from agent.llm import call_llm
from agent.prompts import load_prompt
from agent import tools

class Executor:
    def execute(self, step: str):
        prompt = load_prompt("executor").replace("{step}", step)

        result = call_llm(prompt)

        # Simple tool detection (basic version)
        if result.startswith("search("):
            query = result[len("search("):-1]
            return tools.search(query)

        return result
