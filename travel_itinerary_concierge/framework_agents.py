"""Optional Microsoft Agent Framework Magentic orchestration demo.

The Streamlit app uses deterministic worker modules for reliable budget gating.
This optional script demonstrates framework-based multi-agent collaboration.
Set OPENAI_API_KEY in .env, then run: py framework_agents.py
"""
import asyncio, os
from dotenv import load_dotenv
from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from agent_framework.orchestrations import MagenticBuilder

load_dotenv()

async def main():
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY in .env before running this optional demo.")
    client = OpenAIChatClient(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                              api_key=os.environ["OPENAI_API_KEY"])
    flight = Agent(client=client, name="FlightWorker",
        description="Flight research specialist",
        instructions="Compare flight options for the route. State assumptions; never claim live availability.")
    hotel = Agent(client=client, name="HotelWorker",
        description="Hotel research specialist",
        instructions="Suggest suitable hotels and total stay costs. State assumptions; never claim live availability.")
    activity = Agent(client=client, name="ActivityWorker",
        description="Activity specialist",
        instructions="Create a day-by-day activity plan based on traveller interests.")
    budget = Agent(client=client, name="BudgetWorker",
        description="Budget analyst",
        instructions="Audit every proposed cost against the total budget. Reject over-budget proposals and show arithmetic.")
    manager = Agent(client=client, name="PlannerManager",
        instructions="Delegate to specialists, coordinate their work and consolidate a day-by-day trip plan. Never label an over-budget plan approved.")
    workflow = MagenticBuilder(participants=[flight, hotel, activity, budget],
        manager_agent=manager, max_round_count=12, max_stall_count=3).build()
    task = input("Trip request (e.g. Amritsar to Jaipur, 3 days, ₹35,000, 2 travellers, history/food): ")
    async for event in workflow.run(task, stream=True):
        if event.type in ("intermediate", "output"):
            value = getattr(event.data, "text", None)
            print(value if value else event.data, end="\n", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
