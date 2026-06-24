from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HF_DATASET_NAME: str = "ManikaSaini/zomato-restaurant-recommendation"
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    GROQ_TEMPERATURE: float = 0.3
    MAX_CANDIDATES_FOR_LLM: int = 15
    TOP_K_RECOMMENDATIONS: int = 5
    DATA_CACHE_PATH: str = "data/zomato_cache.parquet"

    # Budget thresholds (cost for two in INR)
    BUDGET_LOW_MAX: int = 500
    BUDGET_MEDIUM_MAX: int = 1500

    class Config:
        env_file = ".env"

settings = Settings()
