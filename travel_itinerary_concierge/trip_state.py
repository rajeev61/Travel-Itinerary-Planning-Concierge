from dataclasses import dataclass, field
from typing import List
from models import TravelOption

@dataclass
class TripState:
    total_budget: float
    selected_items: List[TravelOption] = field(default_factory=list)
    spent: float = 0.0
    rejected_items: List[str] = field(default_factory=list)

    @property
    def remaining(self):
        return round(self.total_budget - self.spent, 2)

    def commit(self, item: TravelOption):
        # Only BudgetWorker should call this after approval.
        self.selected_items.append(item)
        self.spent = round(self.spent + item.cost, 2)
