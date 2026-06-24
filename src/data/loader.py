import os
import pandas as pd
from datasets import load_dataset
from src.config import settings

class DatasetLoader:
    @staticmethod
    def load_data() -> pd.DataFrame:
        """Loads data from local cache if exists, else from Hugging Face."""
        if os.path.exists(settings.DATA_CACHE_PATH):
            print(f"Loading dataset from cache: {settings.DATA_CACHE_PATH}")
            return pd.read_parquet(settings.DATA_CACHE_PATH)
        
        print(f"Downloading dataset {settings.HF_DATASET_NAME} from Hugging Face...")
        dataset = load_dataset(settings.HF_DATASET_NAME, split="train")
        df = dataset.to_pandas()
        
        # Ensure data dir exists
        os.makedirs(os.path.dirname(settings.DATA_CACHE_PATH), exist_ok=True)
        df.to_parquet(settings.DATA_CACHE_PATH)
        print("Dataset cached successfully.")
        return df
