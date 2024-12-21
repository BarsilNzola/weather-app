import requests
from django.conf import settings
import random
from datetime import datetime

def get_weather(city):
    api_key = settings.WEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data  # Return the complete response dictionary
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return {'cod': 'error', 'message': str(e)}
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return {'cod': 'error', 'message': 'Invalid JSON response from API'}


def get_city_coordinates(city):
    api_key = settings.WEATHER_API_KEY  # Reuse OpenWeatherMap API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        return lat, lon
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return None, None
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return None, None


def get_historical_weather(city, date):
    lat, lon = get_city_coordinates(city) 
    if lat is None or lon is None: 
        return {'success': False, 'error': 'Unable to get city coordinates'} 
    
    date_str = date.strftime('%Y-%m-%d') 
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={date_str}&end_date={date_str}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Africa/Nairobi" 

    try: 
        response = requests.get(url) 
        response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx) 
        data = response.json()  
        return data # Return the complete response dictionary 
    except requests.exceptions.RequestException as e: 
        print(f"API request error: {e}") 
        return {'success': False, 'error': str(e)} 
    except ValueError as e: 
        print(f"Error parsing JSON response: {e}") 
        return {'success': False, 'error': 'Invalid JSON response from API'}

def clothing_recommendation(temp):
    if temp < 10:
        return "Heavy jacket and gloves."
    elif 10 <= temp < 20:
        return "Sweater and jeans."
    else:
        return "T-shirt and shorts."

def activity_recommendation(weather):
    if 'rain' in weather.lower():
        return "Stay indoors with a book."
    elif 'clear' in weather.lower():
        return "Perfect for a hike!"
    else:
        return "Check updates and plan accordingly."

def travel_tip(weather):
    if 'rain' in weather.lower():
        return "Carry an umbrella and drive cautiously."
    elif 'snow' in weather.lower():
        return "Be prepared for delays; roads may be slippery."
    elif 'clear' in weather.lower():
        return "Perfect weather for a road trip!"
    else:
        return "Check weather updates before traveling."
    
def get_sustainability_tips():
    tips = [
        "Turn off lights and electronics when not in use to save energy.",
        "Use public transportation, carpool, or bike instead of driving alone.",
        "Reduce, reuse, and recycle to minimize waste.",
        "Save water by fixing leaks and using water-efficient appliances.",
        "Switch to renewable energy sources like solar or wind power if possible.",
        "Plant trees and support reforestation initiatives.",
        "Support local and sustainable businesses.",
        "Avoid single-use plastics and opt for reusable alternatives."
    ]
    return random.choice(tips)
