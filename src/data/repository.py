from src.models.restaurant import Restaurant
from src.data.loader import DatasetLoader
from src.data.preprocessor import DataPreprocessor

class RestaurantRepository:
    def __init__(self):
        self._restaurants: list[Restaurant] = []
        self._locations: set[str] = set()
        self._cuisines: set[str] = set()
        self._loaded = False
        
    def load(self):
        if self._loaded:
            return
            
        df = DatasetLoader.load_data()
        self._restaurants = DataPreprocessor.process(df)
        
        # Populate unique metadata for UI dropdowns/filters
        for r in self._restaurants:
            self._locations.add(r.location)
            for c in r.cuisines:
                self._cuisines.add(c)
                
        self._loaded = True
                
    def get_all(self) -> list[Restaurant]:
        if not self._loaded:
            self.load()
        return self._restaurants
        
    def get_locations(self) -> list[str]:
        if not self._loaded:
            self.load()
        return sorted(list(self._locations))
        
    def get_cuisines(self) -> list[str]:
        if not self._loaded:
            self.load()
        return sorted(list(self._cuisines))

# Singleton instance for the application to share memory
repository = RestaurantRepository()
