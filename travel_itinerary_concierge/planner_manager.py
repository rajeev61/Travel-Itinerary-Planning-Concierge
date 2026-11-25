from models import ItineraryDay, TripResult
from trip_state import TripState
from agents.flight_worker import FlightWorker
from agents.hotel_worker import HotelWorker
from agents.activity_worker import ActivityWorker
from agents.budget_worker import BudgetWorker

class PlannerManager:
    """Delegates to specialist workers; every addition passes BudgetWorker."""
    def __init__(self):
        self.flight_worker = FlightWorker()
        self.hotel_worker = HotelWorker()
        self.activity_worker = ActivityWorker()
        self.budget_worker = BudgetWorker()

    def plan(self, request):
        state = TripState(total_budget=request.budget)
        log = []
        flight = hotel = None

        for option in self.flight_worker.find_flights(request):
            ok, message = self.budget_worker.approve_and_add(option, state)
            log.append(message)
            if ok:
                flight = option
                break

        for option in self.hotel_worker.find_hotels(request):
            ok, message = self.budget_worker.approve_and_add(option, state)
            log.append(message)
            if ok:
                hotel = option
                break

        candidates = self.activity_worker.propose_activities(request)
        days = [ItineraryDay(day=i + 1, title=f"Day {i + 1}") for i in range(request.days)]
        for index, day in enumerate(days):
            preferred = candidates[index % len(candidates)]
            ok, message = self.budget_worker.approve_and_add(preferred, state)
            log.append(message)
            if ok:
                day.activities.append(preferred)
                continue
            for alternative in candidates:
                if alternative.id == preferred.id:
                    continue
                ok, message = self.budget_worker.approve_and_add(alternative, state)
                log.append(message)
                if ok:
                    day.activities.append(alternative)
                    break

        result = TripResult(request=request, flight=flight, hotel=hotel, days=days,
            total_cost=round(state.spent, 2), remaining_budget=round(state.remaining, 2),
            rejected_items=state.rejected_items,
            status="Within budget" if state.remaining >= 0 else "Budget exceeded")
        return result, log
