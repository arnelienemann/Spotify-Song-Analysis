import pandas as pd
import streamlit as st
import plotly.express as px

import sys
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
SPOTIFY_CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"

auth_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(auth_manager=auth_manager)
#sp.me

st.header("Spotify Song Analysis")
st.write("Just search for an artist and start analysizing different song features of the artists top-10 songs and their impact on their popularity.")

search_keyword = st.text_input("Enter the artist name here:")

df = pd.DataFrame()

if search_keyword is not None and len(search_keyword) > 0:
    #st.write("Here are some results:")
    search_results = sp.search(q='artist:'+search_keyword, type='artist',limit=10)

    top_artist = search_results["artists"]["items"][0]
    #top_artist

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header(top_artist["name"])
        st.metric("Popularity", top_artist["popularity"])
    with col3:
        st.image(top_artist["images"][0]["url"], width=200)

    top_tracks = sp.artist_top_tracks(top_artist['id'])
    #top_tracks

    top_tracks_idlist = []
    top_tracks_popularity = []
    top_tracks_name = []

    for track in top_tracks["tracks"]:
        #st.write(track["id"])
        top_tracks_idlist.append(track['id'])
        top_tracks_popularity.append(track['popularity'])
        top_tracks_name.append(track["name"])

    analysis = sp.audio_features(top_tracks_idlist)
    df_analysis = pd.DataFrame(analysis)
    df_analysis.index = top_tracks_name
    df_analysis["popularity"] = top_tracks_popularity
    
    df_analysis
    st.subheader("Popularity:")
    st.bar_chart(df_analysis["popularity"])

    #st.subheader("Energy:")
    #st.line_chart(df_analysis["energy"])
    #st.subheader("Loudness:")
    #st.line_chart(df_analysis["loudness"])
    st.subheader("Tempo:")
    st.line_chart(df_analysis["tempo"])

    fig = px.scatter(df_analysis, x="tempo", y="popularity", trendline="ols")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Danceability:")
    st.line_chart(df_analysis["danceability"])
    fig2 = px.scatter(df_analysis, x="danceability", y="popularity", trendline="ols")
    st.plotly_chart(fig2, use_container_width=True)

    #sp.audio_analysis(track_id)
    #sp.audio_features(tracks=[])


#python -m streamlit run app.py
