from fastapi import APIRouter, HTTPException
from src.models.preferences import UserPreferences
from src.models.recommendation import RecommendationResponse
from src.services.recommendation import RecommendationService
from src.data.repository import repository

router = APIRouter()

# Instantiate the service using the singleton repository
recommendation_service = RecommendationService(repository)

@router.post("/recommendations", response_model=RecommendationResponse)
def get_recommendations(preferences: UserPreferences):
    try:
        return recommendation_service.get_recommendations(preferences)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metadata/locations", response_model=list[str])
def get_locations():
    return repository.get_locations()

@router.get("/metadata/cuisines", response_model=list[str])
def get_cuisines():
    return repository.get_cuisines()
