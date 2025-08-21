import pandas as pd
from src.extract.extract_tracks import extract_tracks
# Extract data
def extract_data() -> tuple[pd.DataFrame]:
    try:
        tracks = extract_tracks()
        # Check if data was extracted successfully
        print(f"Data Extraction was successfully")
        print(f"Tracks: {tracks.shape}")
        return(tracks)
    except Exception as e:
        print(f"Data extraction has failed: {str(e)}")
        