from django.urls import path
from .views import get_players, get_standings

urlpatterns = [
    path('api/players/', get_players, name='get-players'),
    path('api/standings/<str:standing_type>/', get_standings, name='get_pl_standings')
]
