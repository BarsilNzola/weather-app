from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.community_home, name='community_home'),
    path('report/', views.report_event, name='report_event'),
]
