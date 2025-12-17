from app_weather.views import weather_view
from django.urls import path


urlpatterns = [
    path('', weather_view),
]