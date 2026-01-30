# # agent/planner.py

# from agent.prompts import load_prompt

# class Planner:
#     def create_plan(self, goal: str):
#         prompt = load_prompt("planner")
#         prompt = prompt.replace("{goal}", goal)

#         # For now, fake LLM output
#         print("\n🧠 PLANNER PROMPT:\n", prompt)

#         return [
#             "Search information about AI agents",
#             "Summarize key points"
#         ]

from agent.llm import call_llm
from agent.prompts import load_prompt

class Planner:
    def create_plan(self, goal: str):
        prompt = load_prompt("planner").replace("{goal}", goal)

        raw_plan = call_llm(prompt)

        # Convert numbered list → Python list
        steps = [
            line.strip("0123456789. ")
            for line in raw_plan.splitlines()
            if line.strip()
        ]

        return steps
