# api/urls/match.py
from django.urls import path
from ..views.match.info import MatchInformationView
from ..views.match.lineups import MatchLineupsView

urlpatterns = [
    path('match-info/<int:match_id>/',
         MatchInformationView.as_view(),
         name='match-data'),
    
    path('match-lineups/<int:match_id>/',
         MatchLineupsView.as_view(),
         name='match-lineups'),
]