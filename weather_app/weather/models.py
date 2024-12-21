from django.db import models

class SustainabilityTip(models.Model):
    weather_condition = models.CharField(max_length=50)
    tip = models.TextField()

    def __str__(self):
        return self.weather_condition

class WeatherData(models.Model):
    location = models.CharField(max_length=100)
    date = models.DateField()
    temperature = models.FloatField()
    condition = models.CharField(max_length=50)  # e.g., 'Sunny', 'Rainy'

    def __str__(self):
        return f"{self.location} - {self.date}"

class Recommendation(models.Model):
    location = models.CharField(max_length=100)
    activity = models.CharField(max_length=255)
    clothing = models.CharField(max_length=255)
    travel_tip = models.TextField()

    def __str__(self):
        return f"Recommendations for {self.location}"