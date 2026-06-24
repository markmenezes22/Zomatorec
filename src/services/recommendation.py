import json
import logging
from typing import List, Dict, Any
from src.models.restaurant import Restaurant
from src.models.preferences import UserPreferences
from src.models.recommendation import (
    Recommendation, 
    RecommendationResponse, 
    RawLLMResponse
)
from src.services.filter import RestaurantFilter
from src.services.prompt_builder import PromptBuilder
from src.services.llm_client import GroqClient
from src.config import settings

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self, repository):
        """
        Initialize with a RestaurantRepository instance.
        """
        self.repository = repository
        self.llm_client = GroqClient()

    def get_recommendations(self, preferences: UserPreferences) -> RecommendationResponse:
        """
        Orchestrates preference-based filtering, LLM ranking/explanations,
        and response enrichment. Falls back to heuristic ranking if the LLM fails.
        """
        # 1. Retrieve all preprocessed restaurants from repository
        all_restaurants = self.repository.get_all()
        
        # 2. Filter candidates deterministically to get a shortlisted set
        restaurant_filter = RestaurantFilter(all_restaurants)
        candidates = restaurant_filter.filter_candidates(
            preferences, 
            top_k=settings.MAX_CANDIDATES_FOR_LLM
        )
        
        # Prepare metadata
        metadata = {
            "candidates_considered": len(candidates),
            "filters_applied": preferences.model_dump(exclude_none=True),
            "model": settings.GROQ_MODEL,
            "fallback_used": False
        }
        
        # If no candidates matched deterministic filters, return early
        if not candidates:
            return RecommendationResponse(
                summary="No restaurants matched your filters. Please try relaxing your constraints (e.g. broadening your location or budget tier).",
                recommendations=[],
                metadata=metadata
            )
            
        # 3. Call LLM for personalized ranking and explanation
        try:
            system_prompt = PromptBuilder.build_system_prompt()
            user_prompt = PromptBuilder.build_user_prompt(
                preferences, 
                candidates, 
                top_k=settings.TOP_K_RECOMMENDATIONS
            )
            
            # Send to Groq
            raw_response = self.llm_client.get_recommendations(system_prompt, user_prompt)
            
            # Parse raw response
            parsed_data = json.loads(raw_response)
            
            # Validate response matching the raw LLM response schema
            validated_llm_response = RawLLMResponse.model_validate(parsed_data)
            
            # 4. Enrich recommendations with full structured details from the dataset
            enriched_recommendations = self._enrich_recommendations(
                validated_llm_response.recommendations, 
                candidates
            )
            
            # If the LLM returned nothing or all IDs failed to map (edge case), raise error to trigger fallback
            if not enriched_recommendations:
                raise ValueError("LLM response did not map to any valid candidate IDs.")
            
            return RecommendationResponse(
                summary=validated_llm_response.summary,
                recommendations=enriched_recommendations,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error during LLM recommendation generation: {e}. Falling back to heuristic ranking.")
            metadata["fallback_used"] = True
            metadata["fallback_reason"] = str(e)
            return self._generate_heuristic_fallback(candidates, metadata)

    def _enrich_recommendations(
        self, 
        raw_recs: List[Any], 
        candidates: List[Restaurant]
    ) -> List[Recommendation]:
        """
        Combines the LLM's rank and explanation with structured details from the database.
        Ensures uniqueness and limits to top 5 recommendations.
        """
        # Create map of candidates for fast lookup
        candidate_map = {r.id: r for r in candidates}
        enriched = []
        seen_ids = set()
        seen_names = set()
        
        # Sort raw recommendations by LLM's rank to prioritize the best ones
        sorted_raw_recs = sorted(raw_recs, key=lambda x: x.rank)
        
        for raw_rec in sorted_raw_recs:
            if raw_rec.id in seen_ids:
                continue
                
            restaurant = candidate_map.get(raw_rec.id)
            if not restaurant:
                logger.warning(f"LLM recommended an ID not present in candidates list: {raw_rec.id}")
                continue
                
            if restaurant.name in seen_names:
                continue
                
            seen_ids.add(raw_rec.id)
            seen_names.add(restaurant.name)
            
            enriched.append(Recommendation(
                id=restaurant.id,
                rank=len(enriched) + 1,  # Sequential rank after deduplication
                name=restaurant.name,
                cuisine=", ".join(restaurant.cuisines),
                rating=restaurant.rating,
                estimated_cost=restaurant.cost_for_two,
                explanation=raw_rec.explanation
            ))
            
            if len(enriched) >= settings.TOP_K_RECOMMENDATIONS:  # Enforce limit using settings
                break
            
        return enriched

    def _generate_heuristic_fallback(
        self, 
        candidates: List[Restaurant], 
        metadata: Dict[str, Any]
    ) -> RecommendationResponse:
        """
        Fallback recommendation generator when the LLM is down or rate-limited.
        Uses the top heuristic matches with templated explanations.
        """
        fallback_recs = []
        seen_names = set()
        
        for r in candidates:
            if r.name in seen_names:
                continue
                
            explanation = (
                f"Highly rated option ({r.rating}★ with {r.votes} reviews) located in {r.location}. "
                f"Fits your '{r.budget_tier}' budget tier (avg cost {r.cost_for_two} INR for two people)."
            )
            fallback_recs.append(Recommendation(
                id=r.id,
                rank=len(fallback_recs) + 1,
                name=r.name,
                cuisine=", ".join(r.cuisines),
                rating=r.rating,
                estimated_cost=r.cost_for_two,
                explanation=explanation
            ))
            seen_names.add(r.name)
            
            if len(fallback_recs) >= settings.TOP_K_RECOMMENDATIONS:
                break
            
        summary = (
            "Note: The AI recommender is currently offline. "
            "Here are the top-rated matching restaurants based on your constraints."
        )
        
        return RecommendationResponse(
            summary=summary,
            recommendations=fallback_recs,
            metadata=metadata
        )
