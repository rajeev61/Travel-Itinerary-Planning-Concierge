# Travel Itinerary Planning Concierge

A modular multi-agent travel planner demonstrating manager-worker delegation.

## Features
- Planner Manager delegates work to Flight, Hotel and Activity workers.
- Budget Worker is the mandatory gate for every addition to shared trip state.
- Shared in-memory TripState tracks selected items, committed spend and remaining budget.
- Generates a day-by-day itinerary and budget report.
- Runs with sample data and no API key.
- Optional Microsoft Agent Framework Magentic orchestration demo.

> Prices are illustrative academic demo data, not live inventory or bookable quotes.

## Architecture

```text
User / Streamlit UI
        |
  Planner Manager
   /     |      \
Flight  Hotel  Activity
Worker  Worker  Worker
   \     |      /
    Budget Worker  <-- mandatory approval for every addition
          |
     Shared TripState
          |
 Day-by-day itinerary
```

## Run on Windows PowerShell

```powershell
cd travel_itinerary_concierge
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501.

## Demo input
- From: Amritsar
- Destination: Jaipur
- Days: 3
- Budget: ₹35,000
- Travellers: 2
- Interests: history, food, culture

Lower the budget to observe Budget Worker rejections.

## Modules
- `planner_manager.py`: orchestration and delegation.
- `agents/flight_worker.py`: flight candidate search.
- `agents/hotel_worker.py`: hotel candidate search.
- `agents/activity_worker.py`: interest-based activities.
- `agents/budget_worker.py`: approval/rejection gate.
- `trip_state.py`: shared trip memory.
- `data/catalog.py`: replaceable demo data provider.
- `framework_agents.py`: optional Microsoft Agent Framework Magentic demo.

## Budget safety
Workers only propose options. They cannot add items to state. The manager must call
`BudgetWorker.approve_and_add()` for every flight, hotel or activity. Rejected items
are not committed.

## Live data extension
Replace `data/catalog.py` with licensed provider adapters such as Amadeus/Duffel
for flights, hotel partner APIs for stays, and Viator/GetYourGuide partner APIs
for activities. Verify taxes, baggage, cancellation terms and availability before booking.
