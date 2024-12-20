from django.db import models
from django.contrib.auth.models import User

class WeatherEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50, choices=[
        ('hail', 'Hail'),
        ('flood', 'Flood'),
        ('storm', 'Storm'),
        ('heatwave', 'Heatwave'),
    ])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_type} at {self.location} by {self.user.username}"

class CommunityTip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
