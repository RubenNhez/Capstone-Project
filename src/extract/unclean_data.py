import pandas as pd
import numpy as np
from random import choice
from datetime import datetime
## Unclean my CSV clean data 

input_path = r"tracks_features.csv"
output_path = r"data\raw\uncleaned_tracks_features.csv"


# Nulls to add
null_counter = 1000

# Duplicates to add
duplicate_counter = 70

# Data formats
formats = [
    "%Y/%m/%d",
    "%Y-%m-%d",
    "%d %b %Y",
    "%b %d, %Y",
    "%d %B %Y",
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%d/%m/%Y",
]



# Add duplicates

# Randomize release dates
def randomize_format_date(date_str):
    try:
        date_obj = datetime.strptime(str(date_str), "%Y-%m-%d")
        return date_obj.strftime(choice(formats))
    except:
        return date_str


def unclean_data():
    
    # Load data
    df = pd.read_csv(input_path)
    duplicates = df.sample(duplicate_counter,random_state=1).copy()
    duplicates["release_date"] = duplicates["release_date"].apply(randomize_format_date)


    # Add rows with nulls
    nulls_rows = df.sample(null_counter, random_state=2).copy()

    # Random columns to nullify in each row
    cols_to_null = ["name", "album", "release_date","album_id","artists","artist_ids","track_number","disc_number","explicit","danceability","energy","key","loudness","mode","speechiness","acousticness","instrumentalness","liveness","valence","tempo","duration_ms","time_signature","year"]
    for col in cols_to_null:
        idx_to_null = np.random.choice(nulls_rows.index, size=int(null_counter/len(cols_to_null)), replace=False)
        nulls_rows.loc[idx_to_null,col]=np.nan

    #Combine everything
    df_unclean = pd.concat([df,duplicates,nulls_rows], ignore_index=True)
    # Save the unclean dataset
    df_unclean.to_csv(output_path, index=False)
    print(f"Unclean dataset saved to: {output_path}")
