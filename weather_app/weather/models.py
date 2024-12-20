from django.db import models
from django.contrib.auth.models import User

class SustainabilityTip(models.Model):
    weather_condition = models.CharField(max_length=50)
    tip = models.TextField()

    def __str__(self):
        return self.weather_condition

class Badge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    badge_name = models.CharField(max_length=50)
    earned_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.badge_name} - {self.user.username}"
