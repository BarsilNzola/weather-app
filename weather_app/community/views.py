from django.shortcuts import render, redirect
from .models import WeatherEvent, CommunityTip

def community_home(request):
    events = WeatherEvent.objects.all().order_by('-created_at')[:10]  # Limit to latest 10
    tips = CommunityTip.objects.all().order_by('-created_at')[:10]  # Limit to latest 10
    return render(request, 'community/community_home.html', {
        'events': events, 
        'tips': tips, 
    })

def report_event(request):
    if request.method == 'POST':
        name = request.POST['name']
        location = request.POST['location']
        event_type = request.POST['event_type']
        description = request.POST['description']

        # Create the WeatherEvent instance
        WeatherEvent.objects.create(
            name=name, location=location, event_type=event_type, description=description
        )

        return redirect('community:community_home')

    return render(request, 'community/report_event.html')
