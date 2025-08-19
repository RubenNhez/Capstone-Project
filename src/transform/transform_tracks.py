import pandas as pd


def clean_tracks(tracks: pd.DataFrame) -> pd.DataFrame:
    
    # Standardize dates
    tracks = standardize_date_format(tracks)
    # Remove rows with missing values
    tracks = remove_missing_values(tracks)
    # Remove duplicates rows
    tracks = drop_duplicates(tracks)
    # Reset the indexes
    tracks.reset_index(drop=True, inplace=True)
    # Save the dataframe as a CSV
    # Save at least 10,0000 records of the cleaned CSV
    limit_tracks = tracks.head(11000)
    output_path = r"data\processed\cleaned_tracks_features.csv"
    limit_tracks.to_csv(output_path, index=False)
    
    return limit_tracks
    
def remove_missing_values(tracks: pd.DataFrame) -> pd.DataFrame:
    return tracks.dropna(subset=['id', 'name', 'album', 'album_id', 'artists', 'artist_ids', 'track_number', 'disc_number', 'explicit', 'danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature', 'year', 'release_date'])

def drop_duplicates(tracks: pd.DataFrame) -> pd.DataFrame:
    return tracks.drop_duplicates()

def standardize_date_format(tracks: pd.DataFrame) -> pd.DataFrame:
    # Convert all dates to YYYY-MM-DD format
    def standardize_date(date_str):
        
        if pd.isna(date_str):
            return pd.NaT
        # Turn everything into a string
        date_str = str(date_str).strip()

        if len(date_str) != 10:
            return pd.NaT
        
        formats = [
            "%Y/%m/%d",
            "%Y-%m-%d",
            "%d %b %Y",
            "%b %d, %Y",
            "%d %B %Y",
            "%d-%m-%Y",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%d/%m/%Y"
        ]
        for fmt in formats:
            try:
                return pd.to_datetime(date_str, format=fmt)
            except ValueError:
                continue
        return pd.NaT

    before = len(tracks)

    # Apply the parse_date function to the tracks date column
    tracks["release_date"] = tracks["release_date"].apply(standardize_date)
    tracks = tracks.dropna(subset=["release_date"])

    after = len(tracks)
    print(f"Dropped {before - after} rows")

    tracks["release_date"] = tracks["release_date"].dt.strftime("%Y-%m-%d")
    return tracks

