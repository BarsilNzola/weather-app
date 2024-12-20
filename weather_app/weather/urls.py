from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Import the authentication views

app_name = 'weather'

urlpatterns = [
    path('', views.weather_dashboard, name='dashboard'),  # Main dashboard
    path('alerts/', views.alerts, name='alerts'),  # Personalized alerts
]
