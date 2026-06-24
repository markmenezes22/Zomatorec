import json
from typing import List
from src.models.restaurant import Restaurant
from src.models.preferences import UserPreferences

class PromptBuilder:
    @staticmethod
    def build_system_prompt() -> str:
        """
        Builds the system prompt instructing the LLM on its role, constraints, and JSON response schema.
        """
        return (
            "You are a helpful, professional, and knowledgeable AI restaurant recommendation assistant inspired by Zomato.\n"
            "Your task is to rank the candidate restaurants based on the user's preferences, including any soft/additional preferences.\n\n"
            "Constraints:\n"
            "1. You must ONLY recommend restaurants from the provided list of candidates. Do not fabricate or invent new restaurants.\n"
            "2. You must return your response in structured JSON format matching the following schema:\n"
            "{\n"
            "  \"summary\": \"A brief summary (1-2 sentences) explaining the choices and how they match the user's vibe/requirements.\",\n"
            "  \"recommendations\": [\n"
            "    {\n"
            "      \"id\": \"The exact string ID of the restaurant from the candidates list\",\n"
            "      \"rank\": 1,\n"
            "      \"explanation\": \"A personalized explanation of why this restaurant was selected and how it matches the user's explicit or soft preferences.\"\n"
            "    }\n"
            "  ]\n"
            "}\n"
            "Ensure the response is valid JSON. Do not include markdown code block formatting (such as ```json) or any conversational text outside of the JSON."
        )

    @staticmethod
    def build_user_prompt(preferences: UserPreferences, candidates: List[Restaurant], top_k: int = 5) -> str:
        """
        Formats user preferences and candidate restaurants into the user prompt.
        """
        # Convert candidates to a lightweight format to save context window tokens
        candidate_list = []
        for r in candidates:
            candidate_list.append({
                "id": r.id,
                "name": r.name,
                "location": r.location,
                "cuisines": r.cuisines,
                "cost_for_two": r.cost_for_two,
                "rating": r.rating,
                "votes": r.votes,
                "rest_type": r.rest_type,
                "budget_tier": r.budget_tier
            })
            
        pref_dict = {
            "location": preferences.location,
            "budget_tier": preferences.budget_tier,
            "min_rating": preferences.min_rating,
            "preferred_cuisines": preferences.preferred_cuisines,
            "specific_requirements": preferences.specific_requirements
        }
        
        return (
            "Rank the top {k} restaurants from the provided candidates list that best match the user_preferences.\n\n"
            "User Preferences:\n"
            "{user_prefs_json}\n\n"
            "Candidate Restaurants (List of {num_candidates}):\n"
            "{candidates_json}\n\n"
            "Instructions:\n"
            "1. Select and rank up to {k} restaurants from the candidate list. Do not exceed {k}.\n"
            "2. Rank them based on how well they match the preferences. Pay special attention to 'specific_requirements' (like 'family-friendly', 'quick service', 'rooftop', 'romantic', etc.) as soft ranking signals.\n"
            "3. If candidate cuisines or budget tiers don't exactly match but are close, explain why they might be a good fit.\n"
            "4. Provide a distinct 'explanation' for each recommendation, referencing the user's specific request.\n"
            "5. Return only valid JSON matching the system schema."
        ).format(
            k=top_k,
            num_candidates=len(candidates),
            user_prefs_json=json.dumps(pref_dict, indent=2),
            candidates_json=json.dumps(candidate_list, indent=2)
        )
