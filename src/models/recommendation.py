from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# Schema for the raw JSON response returned by the LLM
class RawLLMRecommendation(BaseModel):
    id: str = Field(..., description="The restaurant ID from the candidates list")
    rank: int = Field(..., description="Assigned rank (1 to K)")
    explanation: str = Field(..., description="Specific reason why this restaurant was chosen based on user preferences")

class RawLLMResponse(BaseModel):
    summary: Optional[str] = Field(None, description="Optional brief summary introducing the recommendations")
    recommendations: List[RawLLMRecommendation] = Field(..., description="List of recommended restaurant IDs and their explanations")

# Schema for the enriched response returned to the UI/client
class Recommendation(BaseModel):
    id: str = Field(..., description="The stable identifier matching the database ID")
    rank: int = Field(..., description="Rank assigned (1-based)")
    name: str = Field(..., description="Name of the restaurant")
    cuisine: str = Field(..., description="Comma-separated cuisines of the restaurant")
    rating: float = Field(..., description="Rating of the restaurant")
    estimated_cost: int = Field(..., description="Estimated cost for two in INR")
    explanation: str = Field(..., description="AI-generated explanation of why this restaurant fits the preferences")

class RecommendationResponse(BaseModel):
    summary: Optional[str] = Field(None, description="AI-generated summary introducing the recommendations")
    recommendations: List[Recommendation] = Field(..., description="Ranked list of recommended restaurants with metadata and explanations")
    metadata: Dict = Field(default_factory=dict, description="Metadata about candidates considered, filters applied, and model used")
