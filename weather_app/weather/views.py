from django.shortcuts import render
from .utils import get_weather, clothing_recommendation, activity_recommendation
from .models import SustainabilityTip, Badge

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

def award_badge(user, badge_name):
    """
    Awards a badge to a user if the badge doesn't already exist.
    """
    if not Badge.objects.filter(user=user, badge_name=badge_name).exists():
        Badge.objects.create(user=user, badge_name=badge_name)

# Example: Call this inside a view function
def dashboard(request):
    if request.user.is_authenticated:
        award_badge(request.user, "Weather Guru")
    return render(request, "dashboard.html")
