from django.urls import path
from .views import get_players

urlpatterns = [
    path('api/players/', get_players, name='get-players'),
]
