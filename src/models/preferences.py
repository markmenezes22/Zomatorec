from pydantic import BaseModel, Field
from typing import Optional

class UserPreferences(BaseModel):
    location: str = Field(..., description="The geographical location to search within")
    budget_tier: Optional[str] = Field(None, description="Budget tier: 'Low', 'Medium', or 'High'")
    min_rating: Optional[float] = Field(None, ge=0.0, le=5.0, description="Minimum acceptable rating")
    preferred_cuisines: list[str] = Field(default_factory=list, description="List of preferred cuisines")
    specific_requirements: Optional[str] = Field(None, description="Any other specific constraints or requests")
