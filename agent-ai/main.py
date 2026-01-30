# # main.py

# from agent.planner import Planner
# from agent.executor import Executor
# from agent.observer import Observer
# from agent.memory import Memory

# def main():
#     goal = "AI agents"

#     planner = Planner()
#     executor = Executor()
#     observer = Observer()
#     memory = Memory()

#     print(f"\n🎯 Goal: {goal}\n")

#     plan = planner.create_plan(goal)

#     for step in plan:
#         print(f"➡️ Step: {step}")

#         result = executor.execute(step)
#         print(f"   Result: {result}")

#         status = observer.observe(step, result)
#         print(f"   Status: {status}\n")

#         memory.add(f"{step} => {result} ({status})")

#     print("🧠 Memory:")
#     for log in memory.get_all():
#         print(" -", log)

# if __name__ == "__main__":
#     main()


from agent.planner import Planner
from agent.executor import Executor
from agent.observer import Observer
from agent.memory import Memory

def main():
    goal = "Explain AI agents simply"

    planner = Planner()
    executor = Executor()
    observer = Observer()
    memory = Memory()

    plan = planner.create_plan(goal)

    for step in plan:
        print(f"\n➡️ Step: {step}")

        result = executor.execute(step)
        print("Result:", result)

        status = observer.observe(step, result)
        memory.add(f"{step} => {result} ({status})")

    print("\n🧠 Final Memory:")
    for m in memory.get_all():
        print("-", m)

if __name__ == "__main__":
    main()
