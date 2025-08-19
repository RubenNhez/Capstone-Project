import pandas as pd
from typing import Tuple
from src.transform.transform_tracks import clean_tracks


def transform_data(data) -> Tuple[pd.DataFrame]:
    try:
        print("Starting data transformation process")
        # Clean tracks data
        cleaned_tracks = clean_tracks(data)
        print("Data Transformation was successful")
        return cleaned_tracks
    except Exception as e:
        print(f"Data transformation has failed {str(e)}")
        raise
