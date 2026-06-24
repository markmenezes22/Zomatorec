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
        
        # Keep only required columns to drastically reduce memory usage
        required_columns = ['name', 'location', 'cuisines', 'approx_cost(for two people)', 'rate', 'votes', 'rest_type']
        columns_to_remove = [col for col in dataset.column_names if col not in required_columns]
        dataset = dataset.remove_columns(columns_to_remove)
        
        df = dataset.to_pandas()
        
        # Ensure data dir exists
        os.makedirs(os.path.dirname(settings.DATA_CACHE_PATH), exist_ok=True)
        df.to_parquet(settings.DATA_CACHE_PATH)
        print("Dataset cached successfully.")
        return df
