from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .utils import get_weather, clothing_recommendation, activity_recommendation, travel_tip
from .models import SustainabilityTip, Badge, WeatherData

def weather_dashboard(request):
    weather_data = None
    recommendations = {
        'clothing': "No recommendation available.",
        'activities': "No recommendation available.",
        'travel': "No recommendation available.",
    }
    error_message = None
    city = "Nairobi"  # Default city

    if request.method == 'POST':
        city = request.POST.get('city', 'Nairobi')  # Get city name from form input

    # Fetch weather data
    weather_data = get_weather(city)
    print(f"Raw weather data from API: {weather_data}")

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
        
    # Fetch historical weather data
    historical_data = WeatherData.objects.values('location', 'date', 'temperature', 'condition').order_by('-date')
    historical_data_json = json.dumps(list(historical_data), cls=DjangoJSONEncoder)

    context = {
        'weather': weather_data,
        'recommendations': recommendations,
        'location': city,
        'latitude': latitude,
        'longitude': longitude,
        'historical_data': historical_data_json,
        'WEATHER_API_KEY': settings.WEATHER_API_KEY,
        'error_message': error_message,
    }
    print(f"Context passed to template: {context}")
    return render(request, 'weather/dashboard.html', context)

def award_badge(user, badge_name):
    """
    Awards a badge to a user if the badge doesn't already exist.
    """
    if not Badge.objects.filter(user=user, badge_name=badge_name).exists():
        Badge.objects.create(user=user, badge_name=badge_name)

# Alerts view
@login_required
def alerts(request):
    return render(request, 'weather/alerts.html')
