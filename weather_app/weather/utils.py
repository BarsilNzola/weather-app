import requests
from django.conf import settings

def get_weather(city):
    api_key = settings.WEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    
    print(f"Making API request to: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        print(f"API Response: {data}")
        return data  # Return the complete response dictionary
    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return {'cod': 'error', 'message': str(e)}
    except ValueError as e:
        print(f"Error parsing JSON response: {e}")
        return {'cod': 'error', 'message': 'Invalid JSON response from API'}


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

