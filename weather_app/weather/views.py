from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
import json
from django.shortcuts import render
from datetime import timedelta
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .utils import get_weather, get_historical_weather, clothing_recommendation, activity_recommendation, travel_tip, get_sustainability_tips
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
    
        
    # Fetch historical weather data
    historical_data = WeatherData.objects.filter(date__range=(two_weeks_ago, current_date)).order_by('-date')    
    
    # Convert to JSON
    historical_data_dicts = list(historical_data.values('location', 'date', 'temperature', 'condition')) 
    historical_data_json = json.dumps(historical_data_dicts, cls=DjangoJSONEncoder)
    
    # Other context data
    sustainability_tips = get_sustainability_tips()
    
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
