from django.urls import path
from .views import (
    CompetitionsView,
    SeasonsView,
    TouchDataView,
    LeagueMatchesView,
    CompetitionInfoView,
    MatchLineupsView
)

urlpatterns = [
    # Core endpoints needed for LeagueOverview component
    path('api/matches/<int:competition_id>/<int:season_id>/',
         LeagueMatchesView.as_view(),
         name='league-matches'),

    path('api/competition-info/<int:competition_id>/<int:season_id>/',
         CompetitionInfoView.as_view(),
         name='competition-info'),

    # Supporting endpoints
    path('api/competitions/',
         CompetitionsView.as_view(),
         name='competitions'),

    path('api/seasons/<int:competition_id>/',
         SeasonsView.as_view(),
         name='seasons'),

    path('api/touches/<int:match_id>/<str:player_name>/',
         TouchDataView.as_view(),
         name='touch-data'),

    path('api/lineups/<int:match_id>/',
         MatchLineupsView.as_view(),
         name='match-lineups'),
]
