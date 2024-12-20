import requests
from django.conf import settings

def get_weather(city):
    api_key = settings.WEATHER_API_KEY
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    return response.json()

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
