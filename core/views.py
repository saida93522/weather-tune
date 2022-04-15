import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.html import format_html
from core.API import spotifyApi as sp
from core.API import weatherApi as wd
import spotipy
import uuid
from .credentials import SPOTIPY_REDIRECT_URI, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SCOPE

caches_folder = './.spotify_caches/'
if not os.path.exists(caches_folder):
    os.makedirs(caches_folder)

def session_cache_path(request):
    session_id = request.session.get('uuid')
    return caches_folder + str(session_id)

def authenticate(request):
    if not request.session.get('uuid'):
        request.session['uuid'] = str(uuid.uuid4())

    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(request))
    oauth_sp = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI,scope=SCOPE, cache_handler=cache_handler,show_dialog=True)
    code = oauth_sp.get_authorization_code()
    if code:
        oauth_sp.get_access_token(code)
        return redirect('home')
    if not oauth_sp.validate_token(cache_handler.get_cached_token()):
        auth_url = oauth_sp.get_authorize_url()
        return format_html('<a href="{}">Sign in</a>',auth_url)
    # spotify object
    st = spotipy.Spotify(auth_manager=sp_token)
    username = st.me()
    context = {
        'username':username
    }

    return render(request,'home2.html',context)



def home(request):
    cache_handler = spotipy.cache_handler.CacheFileHandler(cache_path=session_cache_path(request))
    oauth_sp = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI,cache_handler=cache_handler)
    if not oauth_sp.validate_token(cache_handler.get_cached_token()):
        return redirect('auth_spotify')
    spotify = spotipy.Spotify(auth_manager=oauth_sp)
    username = spotify.current_user()
    weather_data = wd.user_location()
    weather_id = weather_data["weather"][0]['id']
    playlist_id = sp.play_playlist(spotify,username['id'],weather_id)
    
    context ={
        'current_user': username['id'],
        'playlist_id':playlist_id,
        'country':str(weather_data['sys']['country']),
        'weather_temp':str(int(weather_data["main"]['temp'])),
        'main':str(weather_data['main']['feels_like']),
        'weather_description':str(weather_data["weather"][0]['description']),
        'city':str(weather_data['name']),
        }
    return render(request,'home.html',context)




