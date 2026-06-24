import pandas as pd
from src.config import settings
from src.models.restaurant import Restaurant

class DataPreprocessor:
    @staticmethod
    def process(df: pd.DataFrame) -> list[Restaurant]:
        """Cleans and maps raw dataframe into a list of Restaurant objects."""
        # Rename columns to standard if needed based on the HF dataset structure
        col_mapping = {
            'approx_cost(for two people)': 'cost_for_two',
            'rate': 'rating'
        }
        df = df.rename(columns=col_mapping)
        
        restaurants = []
        for index, row in df.iterrows():
            try:
                # Basic cleaning
                name = str(row.get('name', '')).strip()
                location = str(row.get('location', '')).strip().title()
                
                # Cuisines
                cuisines_str = str(row.get('cuisines', ''))
                cuisines = [c.strip() for c in cuisines_str.split(',') if c.strip()]
                
                # Cost
                cost_str = str(row.get('cost_for_two', '0'))
                cost_str = cost_str.replace(',', '').strip()
                cost = int(cost_str) if cost_str.isdigit() else 0
                
                # Rating (often comes as '4.1/5')
                rating_str = str(row.get('rating', '0'))
                if '/' in rating_str:
                    rating_str = rating_str.split('/')[0].strip()
                try:
                    rating = float(rating_str)
                except ValueError:
                    rating = 0.0
                    
                # Votes
                votes_val = row.get('votes', 0)
                try:
                    votes = int(votes_val)
                except ValueError:
                    votes = 0
                    
                rest_type = str(row.get('rest_type', '')).strip()
                
                # Hard skip for entirely invalid rows
                if not name or not location or cost <= 0:
                    continue
                    
                # Determine Budget Tier
                if cost <= settings.BUDGET_LOW_MAX:
                    budget_tier = "low"
                elif cost <= settings.BUDGET_MEDIUM_MAX:
                    budget_tier = "medium"
                else:
                    budget_tier = "high"
                    
                rest = Restaurant(
                    id=str(index),
                    name=name,
                    location=location,
                    cuisines=cuisines,
                    cost_for_two=cost,
                    rating=rating,
                    votes=votes,
                    rest_type=rest_type,
                    budget_tier=budget_tier
                )
                restaurants.append(rest)
            except Exception as e:
                # Skip rows that fail processing completely
                continue
                
        return restaurants
