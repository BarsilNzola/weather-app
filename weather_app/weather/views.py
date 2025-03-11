import requests
from .utils import get_weather, get_historical_weather, clothing_recommendation, activity_recommendation, travel_tip, get_sustainability_tips, get_city_coordinates
from weather.models import SustainabilityTip, WeatherData
from django.utils.timezone import now
from datetime import timedelta
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render

# Function to get city based on user's IP address
def get_user_city(request):
    ip = request.META.get('REMOTE_ADDR')
    response = requests.get(f"http://ip-api.com/json/{ip}")
    city = response.json().get('city', 'Nairobi')  # Default to Nairobi if location is not found
    return city

def weather_dashboard(request):
    weather_data = None
    recommendations = {
        'clothing': "No recommendation available.",
        'activities': "No recommendation available.",
        'travel': "No recommendation available.",
    }
    error_message = None
    
    # Use the city from the form if it exists, else use the IP-based city
    city = request.GET.get('city', get_user_city(request))  # Use GET for API calls

    # Clear existing historical data for the current city 
    WeatherData.objects.filter(location=city).delete()

    # Fetch and store historical data 
    two_weeks_ago = now().date() - timedelta(weeks=2) 
    current_date = now().date() 
    for day in range((current_date - two_weeks_ago).days + 1): 
        date_to_fetch = current_date - timedelta(days=day) 
        historical_data = get_historical_weather(city, date_to_fetch) 
        if historical_data and 'daily' in historical_data: 
            daily_data = historical_data['daily']
            temperature_max = daily_data.get('temperature_2m_max', [None])[0] 
            temperature_min = daily_data.get('temperature_2m_min', [None])[0] 
            if temperature_max is not None and temperature_min is not None: 
                WeatherData.objects.create( 
                    location=city, 
                    date=date_to_fetch, 
                    temperature=temperature_max, # Max temperature for the day 
                    condition='N/A' # Open-Meteo does not provide specific weather conditions 
                )
            else: 
                print(f"No temperature data found for {city} on {date_to_fetch}") 
        else: 
            print(f"No historical weather data found for {city} on {date_to_fetch}")

    # Fetch weather data
    weather_data = get_weather(city)

    if weather_data and weather_data.get('cod') == 200:  # Successful response
        temp = weather_data['main']['temp']
        weather_condition = weather_data['weather'][0]['description']

        recommendations = {
            'clothing': clothing_recommendation(temp),
            'activities': activity_recommendation(weather_condition),
            'travel': travel_tip(weather_condition),
        }
        latitude = weather_data.get('coord', {}).get('lat', 0)
        longitude = weather_data.get('coord', {}).get('lon', 0)
    else:
        print(f"Error fetching weather data: {weather_data.get('message', 'Unknown error')}")
        error_message = weather_data.get('message', "Unable to fetch weather data.")
        latitude = 0
        longitude = 0
    
    # Fetch historical weather data for the current city
    historical_data = WeatherData.objects.filter(location=city, date__range=(two_weeks_ago, current_date)).order_by('-date')    
    
    # Convert to JSON
    historical_data_dicts = list(historical_data.values('location', 'date', 'temperature', 'condition')) 
    historical_data_json = json.dumps(historical_data_dicts, cls=DjangoJSONEncoder)
    
    # Other context data
    sustainability_tips = get_sustainability_tips()
    
    # Prepare response data
    response_data = {
        'weather': weather_data,
        'recommendations': recommendations,
        'location': city,
        'latitude': latitude,
        'longitude': longitude,
        'historical_data': historical_data_json,
        'sustainability_tips': sustainability_tips,
        'error_message': error_message,
    }

    # Return JSON response for API calls
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse(response_data)

    # Render HTML template for web requests
    context = {
        'weather': weather_data,
        'recommendations': recommendations,
        'location': city,
        'latitude': latitude,
        'longitude': longitude,
        'historical_data': historical_data_json,
        'WEATHER_API_KEY': settings.WEATHER_API_KEY,
        'sustainability_tips': sustainability_tips,
        'error_message': error_message,
    }
    return render(request, 'weather/dashboard.html', context)

# Alerts view
def alerts(request):
    return render(request, 'weather/alerts.html')
