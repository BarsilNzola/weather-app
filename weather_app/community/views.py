from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import WeatherEvent, CommunityTip
from weather.models import Badge  # Assuming Badge is in the weather app

def community_home(request):
    events = WeatherEvent.objects.all().order_by('-created_at')
    tips = CommunityTip.objects.all().order_by('-created_at')
    badges = []
    if request.user.is_authenticated:
        badges = Badge.objects.filter(user=request.user)
    return render(request, 'community/community_home.html', {'events': events, 'tips': tips, 'badges': badges})


@login_required
def report_event(request):
    if request.method == 'POST':
        location = request.POST['location']
        event_type = request.POST['event_type']
        description = request.POST['description']

        # Create the WeatherEvent instance
        WeatherEvent.objects.create(
            user=request.user, location=location, event_type=event_type, description=description
        )

        return redirect('community:community_home')

    # Pre-fill the location using weather data (if applicable)
    user_location = "Unknown"
    if request.user.is_authenticated:
        # Example: fetch location from Weather API
        user_location = "New York"  # Replace with dynamic data if available

    return render(request, 'community/report_event.html', {'user_location': user_location})


@login_required
def view_tips(request):
    tips = CommunityTip.objects.all().order_by('-created_at')
    return render(request, 'community/tips.html', {'tips': tips})
