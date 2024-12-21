from django.db import models
from django.utils.timezone import now

class WeatherEvent(models.Model):
    name = models.CharField(max_length=100)  # New field for user's name
    location = models.CharField(max_length=100)
    event_type = models.CharField(max_length=50, choices=[
        ('hail', 'Hail'),
        ('flood', 'Flood'),
        ('storm', 'Storm'),
        ('heatwave', 'Heatwave'),
    ])
    description = models.TextField()
    created_at = models.DateTimeField(default=now)  # Default value

    def __str__(self):
        return f"{self.event_type} at {self.location} by {self.name}"

class CommunityTip(models.Model):
    name = models.CharField(max_length=100)  # New field for user's name
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=now)  # Default value

    def __str__(self):
        return f"{self.title} by {self.name}"
