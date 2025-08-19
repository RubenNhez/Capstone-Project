import os
import pandas as pd
import timeit

# Define the file path for the unclean track features CSV file
FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "data",
    "raw",
    "uncleaned_tracks_features.csv",
)

def extract_tracks() -> pd.DataFrame:
    start_time = timeit.default_timer()
    
    try:
        # Read CSV from the given path
        tracks = pd.read_csv(FILE_PATH)
        extract_tracks_execution_time = timeit.default_timer() - start_time
        # Print extracted tracks if successful
        print(f"Extracted tracks table in: {extract_tracks_execution_time} seconds")
        return tracks
    # Print if tracks extraction was unsuccessful
    except Exception as e:
        print(f"Failed to extract data: {e}")
        raise Exception(f"Failed to extract data:{e}")
        