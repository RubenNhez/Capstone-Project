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
    # Asked ChatGPT how do you change the background color in a streamlit applications
    st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #228B22;
        color: white;
    }
    
    """,
    unsafe_allow_html=True
    )
    st.title("Spotify Insights🕵️")
    # Spotify logo image
    st.image(r"data:image/png;base64,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")

    st.write("Welcome to my Spotify Insights Application where you will receive Artists and User Insights Using the Spotify API using a Simple Artist Comparison, Artist Albums and Singles Counter, a delve into an artist's insights and finally User insights.")
    st.header("✨Contexts✨")
    st.subheader("⚖️Simple Artist Comparison⚖️")
    st.write("- Takes an artist and displays a of 10 list of artists of similar genres for a popularity comparison select who you would like to see.")
    st.subheader("🔢Artist Album and Singles Counter🔢")
    st.write("- Takes an artist and displays a counter of albums and singles throughout the years. (Maximum of last 50 albums/singles)")
    st.subheader("🎵Artist Insights🎵")
    st.write("- Takes an Artist Displays the Top tracks for that artists, compares tracks popularity and how many hits they had per year based on the top tracks")
    st.header("🧑‍⚖️User Insights🧑‍⚖️")
    st.write("- Display a Mini Spotify Wrapped based on either inputs by an user or mine by default")
    st.write("- Last 20 tracks listened to, Last 10 songs/albums listened based on time range: Last 4 weeks,Last 6 months and All time")
elif page == "Simple Artist Comparison":
    st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #228B22;
        color: white;
    }
    
    """,
    unsafe_allow_html=True
    )
    # Spotify API
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id= client_id,
    client_secret= client_secret
))
    # Take user_input to look up an artist
    st.title("Simple Artist Comparison⚖️")
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
    st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #228B22;
        color: white;
    }
    
    """,
    unsafe_allow_html=True
    )
    # Spotify API
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id= client_id,
        client_secret= client_secret
    ))
    
    st.title("Artist Albums and Singles Counter🔢")
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
    st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #228B22;
        color: white;
    }
    
    """,
    unsafe_allow_html=True
    )
    # Title
    st.title("Artist Insights🎵")
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
    st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #B2AC88;
        color: white;
    }
    
    """,
    unsafe_allow_html=True
    )
    st.title("Mini Spotify Wrapped🧑‍⚖️")
    # Spotify API
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id= client_id,
        client_secret= client_secret,
        redirect_uri= redirect_uri,
        scope="user-read-recently-played user-top-read"
    ))
    # Recent Music
    st.subheader("Latest 20 tracks🕔")
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
    
    st.header("Songs🎼")
    
    # Define Date ranges
    time_range = {
        "short_term": "Last 4 weeks⌛",
        "medium_term": "Last 6 months⌛",
        "long_term": "All time⌛"
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
    st.header("Artists🎶")
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

    
    
