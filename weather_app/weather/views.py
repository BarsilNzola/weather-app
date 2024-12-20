from django.shortcuts import render
from .utils import get_weather, clothing_recommendation, activity_recommendation
from .models import SustainabilityTip

def weather_dashboard(request):
    city = request.GET.get('city', 'Nairobi')
    weather = get_weather(city)
    clothing = clothing_recommendation(weather['main']['temp'])
    activity = activity_recommendation(weather['weather'][0]['description'])
    tips = SustainabilityTip.objects.filter(weather_condition=weather['weather'][0]['main'])
    return render(request, 'weather/dashboard.html', {
        'weather': weather,
        'city': city,
        'clothing': clothing,
        'activity': activity,
        'tips': tips,
    })
