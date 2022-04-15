import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import json
import logging
from core.API import weatherApi as wd
import pprint
import uuid

def get_top_tracks(sp):
    results = sp.current_user_top_tracks(limit=1, offset=1, time_range='medium_term')
    
    top_track_data = json.dumps(results['items'],indent=4)
    with open('top_track.json','w') as outfile:
        outfile.write(top_track_data)

    for idx,track in enumerate(results['items']):
        top_track_artist_id = track['album']['artists'][0]['id']
        top_track_id = track['id']
        
    return top_track_artist_id, top_track_id
  

def create_playlist(sp,user_id):
    # if logged in get users
    user = sp.user(user=user_id)
    if user != None:
        new_playlist = sp.user_playlist_create(user=user_id, name='weather_playlist', public=True, collaborative=False, description='Songs for weather',)
        
        return new_playlist['id']
    else:
        None
  

def add_tracks_to_playlist(sp,playlist_id,song_uri):
    playlist = sp.playlist_add_items(playlist_id=playlist_id,items=song_uri,position=None)
    return playlist

           
def get_recommendations(sp,weather_id):
    limit = 1
    seed_artist_id = get_top_tracks(sp)[0]
    seed_tracks_id = get_top_tracks(sp)[1]

    sg = wd.get_weather_data_audio(weather_id)[0]
    ta = wd.get_weather_data_audio(weather_id)[1]
    te = wd.get_weather_data_audio(weather_id)[2]
    ti = wd.get_weather_data_audio(weather_id)[3]
    td = wd.get_weather_data_audio(weather_id)[4]
    tv = wd.get_weather_data_audio(weather_id)[5]

    recc = sp.recommendations(limit=50,seed_artists=[seed_artist_id],seed_genres=[sg], seed_tracks=[seed_tracks_id], target_acousticness=ta, target_energy=te,target_instrumentalness=ti,target_danceability=td,target_valence=tv)
    track_uri = []
    for idx, item in enumerate(recc['tracks']):
        track_uri.append(item['uri'])
    playlist_data = json.dumps(track_uri,indent=4)
    with open('playlist.json','w') as outfile:
        outfile.write(playlist_data)
    return track_uri
    
def play_playlist(sp,user_id,weather_id):
    playlist_id = create_playlist(sp,user_id)
    song_uri = get_recommendations(sp,weather_id)
    add_tracks_to_playlist(sp,playlist_id,song_uri)
    
    return playlist_id   