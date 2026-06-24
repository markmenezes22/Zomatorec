from typing import List
from src.models.restaurant import Restaurant
from src.models.preferences import UserPreferences

class RestaurantFilter:
    def __init__(self, restaurants: List[Restaurant]):
        """
        Initialize the filter with a dataset of restaurants.
        """
        self.restaurants = restaurants

    def filter_candidates(self, preferences: UserPreferences, top_k: int = 15) -> List[Restaurant]:
        """
        Apply deterministic filtering based on user preferences and return the top K candidates.
        """
        candidates = self.restaurants
        
        # 1. Filter by location (case-insensitive substring match)
        if preferences.location:
            loc = preferences.location.lower().strip()
            candidates = [r for r in candidates if loc in r.location.lower()]
            
        # 2. Filter by budget tier if specified
        if preferences.budget_tier:
            bt = preferences.budget_tier.lower().strip()
            candidates = [r for r in candidates if r.budget_tier.lower() == bt]
            
        # 3. Filter by minimum rating
        if preferences.min_rating is not None:
            candidates = [r for r in candidates if r.rating >= preferences.min_rating]
            
        # 4. Filter by cuisine (any matching cuisine) if specified
        if preferences.preferred_cuisines:
            pref_cuisines = [c.lower().strip() for c in preferences.preferred_cuisines]
            def matches_cuisine(r: Restaurant) -> bool:
                rest_cuisines = [c.lower().strip() for c in r.cuisines]
                # If any of the preferred cuisines matches any of the restaurant's cuisines
                return any(
                    any(p in rc for p in pref_cuisines) or any(rc in p for p in pref_cuisines)
                    for rc in rest_cuisines
                )
            
            candidates = [r for r in candidates if matches_cuisine(r)]
            
        # 5. Sort by rating (descending) and votes (descending) as a heuristic
        candidates.sort(key=lambda r: (r.rating, r.votes), reverse=True)
        
        # 6. Take Top K
        return candidates[:top_k]
