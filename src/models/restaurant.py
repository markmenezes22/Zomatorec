from pydantic import BaseModel

class Restaurant(BaseModel):
    id: str
    name: str
    location: str
    cuisines: list[str]
    cost_for_two: int
    rating: float
    votes: int = 0
    rest_type: str = ""
    budget_tier: str = ""
