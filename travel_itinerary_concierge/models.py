from pydantic import BaseModel, Field
from typing import List, Optional

class TripRequest(BaseModel):
    origin: str
    destination: str
    days: int = Field(ge=1, le=14)
    budget: float = Field(gt=0)
    travellers: int = Field(ge=1, le=12)
    interests: List[str] = []
    hotel_category: str = "Budget"
    start_date: Optional[str] = None

class TravelOption(BaseModel):
    id: str
    category: str
    name: str
    description: str
    cost: float
    day: Optional[int] = None
    location: Optional[str] = None

class ItineraryDay(BaseModel):
    day: int
    title: str
    activities: List[TravelOption] = []

class TripResult(BaseModel):
    request: TripRequest
    flight: Optional[TravelOption] = None
    hotel: Optional[TravelOption] = None
    days: List[ItineraryDay]
    total_cost: float
    remaining_budget: float
    rejected_items: List[str] = []
    status: str
