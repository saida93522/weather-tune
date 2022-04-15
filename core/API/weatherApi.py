import os
import ipinfo
import requests
import json
from ipify import get_ip
from ipify.exceptions import ConnectionError, ServiceError
from django.conf import settings
from functools import lru_cache
from ..credentials import IP_TOKEN,WEATHER_API



@lru_cache(maxsize=16)
def get_ip_data():
    # get user location using ip address
    try:
        ip_address = get_ip()
        return ip_address
    except IpifyException:
        # If you get here, then some ipify exception occurred.
        print('error ipify')
    except:
        pass
        # some non-ipify related exception occurred.

@lru_cache(maxsize=16)
def get_ip_details():
    ip_data = ipinfo.getHandler(IP_TOKEN)
    ip_address = get_ip_data()
    ip_data = ip_data.getDetails(ip_address)
    return ip_data


def user_location():
    user_loc = get_ip_details()
    if user_loc != None:
        lat = user_loc.latitude
        lon = user_loc.longitude
        return get_weather_data(lat,lon)
    else:
        None


def get_weather_data(lat,lon):
    try:
        weather = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API}&units=imperial')
        
        # convert to dict
        weather_data = json.loads(weather.text)
        return weather_data
    except Exception as e:
        print(e)


def get_weather_data_audio(weather_id):
    #Correlate weather data to spotify audio features   
    
    weather_id_parse = weather_id // 100
    target_danceability = 0
    target_energy = 0
    target_valence = 0
    target_acousticness = 0

    if weather_id == 800:
        # clear sky/sunny day
        weather_code = 0
        
        # audio features
        target_danceability = 1.3
        target_energy = 1.7
        target_valence = 1.6
        target_acousticness = -1.3
        target_instrumentalness = -1.05

        #genre
        genre= 'happy'
        
    elif weather_id_parse == 8:
        # cloudy Day
        weather_code = 1

        # audio features
        target_danceability = -1.2
        target_energy = -1.6
        target_valence = -1.3
        target_acousticness = 1.1
        target_instrumentalness = 1.5

        #genre
        genre= 'chill'
        
    elif weather_id_parse == 2 or weather_id_parse == 3 or weather_id_parse == 5:
        # rainy Day
        weather_code = 2

        # audio features
        target_danceability = -1.3
        target_energy = -1.7
        target_valence = -1.5
        target_acousticness = 1.8
        target_instrumentalness = 1.2

        #genre
        genre= 'rainy-day'
        
    elif weather_id_parse == 6:
        # snowy Day
        weather_code = 3
        
        # audio features
        target_danceability = -1.03
        target_energy = -1.5
        target_valence = -1.15
        target_acousticness = 1.2
        target_instrumentalness = 1.5

        #genre
        genre= 'holidays'
    return genre,target_acousticness, target_energy,target_instrumentalness,target_danceability,target_valence

