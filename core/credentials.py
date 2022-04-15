import os 
IP_TOKEN = os.environ.get('IP_TOKEN')
WEATHER_API = os.environ.get('WEATHER_API')

# spotify
SPOTIPY_CLIENT_ID=os.environ.get('CLIENT_ID')
SPOTIPY_CLIENT_SECRET=os.environ.get('CLIENT_SECRET')
SPOTIPY_REDIRECT_URI=os.environ.get('REDIRECT_URI')
SCOPE = "user-read-recently-played user-read-currently-playing playlist-modify-public playlist-modify-private user-library-read user-library-modify user-top-read playlist-read-private user-read-email"