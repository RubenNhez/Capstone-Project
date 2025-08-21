import os
import spotipy
import streamlit as st 
import pandas as pd 
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# Load credentials
load_dotenv(".env.dev")
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

# Move between pages
page = st.sidebar.selectbox("Select Page", ["Home","Simple Artist Comparison", "Artist Albums and Singles Counter","Artist Insights","User Insights"])
if page == "Home":
    st.title("Spotify Insights")
elif page == "Simple Artist Comparison":
    # Spotify API
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id= client_id,
    client_secret= client_secret
))
    # Take user_input to look up an artist
    query = st.text_input("Look up an artist:")
    #Run query to get artist
    if query:
        results = sp.search(q=query, type="artist",limit=10)
        artists = results.get("artists", {}).get("items", [])
    
        if artists:
            # Make a map to score the names
            artist_names = {artist["name"]: artist for artist in artists}
        
            selected_artist = st.multiselect("Select artist/artists:",list(artist_names.keys()))
        
            data = []
            # Get artist information from the selected artists
            for name in selected_artist:
                artist_data = artist_names[name]
                # Get the name, total of followers, popularity and genres from the artist data
                data.append({
                    "Name": artist_data["name"],
                    "Followers": artist_data["followers"]["total"],
                    "Popularity": artist_data["popularity"],
                    "Genres": ", ".join(artist_data["genres"])
                })
            artist_df = pd.DataFrame(data)    
            st.table(artist_df)
            st.subheader("Artists Popularity")
            st.bar_chart(artist_df.set_index("Name")["Popularity"])

elif page == "Artist Albums and Singles Counter":
    
    # Spotify API
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id= client_id,
        client_secret= client_secret
    ))
    
    st.title("Artist Albums and Singles Counter")
    # Take user input
    query = st.text_input("Look up an Artist:")
    artist_id = None
    
    # search for user input and display matches
    if query:
        results = sp.search(q=query, type="artist", limit=5)
        artists = results.get("artists", {}).get("items", [])

        if artists:
            artists_result = {artist["name"]: artist for artist in artists}
            # Select your artist
            select = st.selectbox("Select Artist:", list(artists_result.keys()))
            artist = artists_result[select]
            
            #Albums
            
            st.subheader("Album Counter")
            albums = []
            # Get a list of albums dictionaries from the items in artists_albums method
            results = sp.artist_albums(artist["id"], album_type="album", limit=50)
            albums = results.get("items", [])
            # Create a dictionary to track how many albums came out in each year
            years_counter = {}
            # Get the album release date and "" if missing
            for album in albums:
                release_date = album.get("release_date", "")
                # Spotify return YYYY-MM-DD format get the first value
                year = release_date.split("-")[0]
                # check if year isn't empty
                # check if year is in dictionary if yes add 1 otherwise add and set default to 1
                if year:
                    years_counter[year] = years_counter.get(year, 0) + 1
            
            
            # Store into a dataframe and display it    
            album_df = pd.DataFrame({
                "Year": list(years_counter.keys()),
                "Number of Albums": list(years_counter.values())
            }).sort_values("Year")
            
            st.dataframe(album_df)
            st.bar_chart(album_df.set_index("Year")["Number of Albums"])
            
            # Singles
            
            st.subheader("Singles Counter")
            singles = []
            # Get a list of singles dictionaries from the items in artists_albums method
            results = sp.artist_albums(artist["id"], album_type="single", limit=50)
            singles = results.get("items", [])
            
            years_counter = {}
            # Get the single release date and "" if missing
            for single in singles:
                release_date = single.get("release_date", "")
                # Spotify return YYYY-MM-DD format 
                year = release_date.split("-")[0]
                # check if year isn't empty
                # check if year is in dictionary if yes add 1 otherwise add and set default to 1
                if year:
                    years_counter[year] = years_counter.get(year, 0) + 1
            
            
            # Store into a dataframe and display it    
            singles_df = pd.DataFrame({
                "Year": list(years_counter.keys()),
                "Number of Singles": list(years_counter.values())
            }).sort_values("Year")
            
            st.dataframe(singles_df)
            st.bar_chart(singles_df.set_index("Year")["Number of Singles"])





elif page == "Artist Insights":
    # Title
    st.title("Artist Insights")
    # Spotify API 
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id= client_id,
        client_secret= client_secret
    ))
    # Search for the artist
    artist_name = st.text_input("Look up an artist:")
    if artist_name:
        results = sp.search(q=artist_name, type="artist",limit=1)
        artists = results.get("artists", {}).get("items", [])
        # Get the artist's name and id from the artists result list
        artist = artists[0]
        artist_name = artist["name"]
        artist_id = artist["id"]
        
        st.subheader(f"Top Tracks for {artist_name}")
        # Top Tracks
        top_tracks_result = sp.artist_top_tracks(artist_id)
        top_tracks = []
        # From the tracks dictionary get the name,album,release date and popularity for that Track
        for track in top_tracks_result["tracks"]:
            top_tracks.append({
                "Track": track["name"],
                "Album": track["album"]["name"],
                "Release Date": track["album"]["release_date"],
                "Popularity": track["popularity"]
            })
        top_tracks_df = pd.DataFrame(top_tracks)
        st.dataframe(top_tracks_df)
        
        # Bar chart on track popularity
        st.subheader("Track Popularity")
        st.bar_chart(top_tracks_df.set_index("Track")["Popularity"])
        
        # Get How many hits they have based on top tracks a year
        st.subheader(f"Hits per year based on top tracks for {artist_name}")
        track_year = []
        for track in top_tracks_result["tracks"]:
            year = track["album"]["release_date"][:4]
            track_year.append(year)
        count = pd.Series(track_year).value_counts().sort_index()
        st.line_chart(count)
        
elif page == "User Insights":
    # Spotify API
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id= client_id,
        client_secret= client_secret,
        redirect_uri= redirect_uri,
        scope="user-read-recently-played user-top-read"
    ))
    st.title("Mini Spotify Wrapped")
    # Recent Music
    st.subheader("Last 20 tracks")
    # Collect last 20 tracks
    recent_tracks = sp.current_user_recently_played(limit=20)
    tracks = []
    # Loop through each track get name, artists,album and store them as a list of dictionaries
    for item in recent_tracks["items"]:
        track = item["track"]
        tracks.append({
            "Track": track["name"],
            "Artist": ", ".join([a["name"] for a in track["artists"]]),
            "Album": track["album"]["name"]
        })
    # Convert to DataFrame and Display table
    recent_tracks_df = pd.DataFrame(tracks)
    st.table(recent_tracks_df)
    
    st.subheader("Top 10 Tracks")
    # Define Date ranges
    time_range = {
        "short_term": "Last 4 weeks",
        "medium_term": "Last 6 months",
        "long_term": "All time"
    }
    # Get top  10 tracks using the Spotify current_user_top_tracks
    for time,label in time_range.items():
        st.subheader(label)
        top_tracks = sp.current_user_top_tracks(limit=10, time_range=time)
        result = []
        # Loop through each track get name, artists, album ,popularity and store them as a list of dictionaries
        for track in top_tracks["items"]:
            result.append({
                "Track": track["name"],
                "Artist": ", ".join([artist["name"] for artist in track["artists"]]),
                "Album": track["album"]["name"],
                "Popularity": track["popularity"]
            })
            
        # Convert to DataFrame and Display table
        result_df = pd.DataFrame(result)
        st.table(result_df)
    
    for time, label in time_range.items():
        st.subheader(label)
        # Get top 10 artists using the Spotify current_user_top_tracks
        top_artists = sp.current_user_top_artists(limit=10, time_range=time)
        
        artists_res = []
        # Loop through each artists get name, genres, popularity, followers and store them as a list of dictionaries
        for artist in top_artists["items"]:
            artists_res.append({
                "Artist": artist["name"],
                "Genres": ", ".join(artist["genres"]),
                "Popularity": artist["popularity"],
                "Followers": artist["followers"]["total"]
            })
        # Convert to DataFrame and Display table
        artists_res_df = pd.DataFrame(artists_res)
        st.table(artists_res_df)

    
    
