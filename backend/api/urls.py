from django.urls import path
from .views import (
    CompetitionsView,
    SeasonsView,
    TouchDataView,
    LeagueMatchesView,
    CompetitionInfoView,
    MatchLineupsView,
    PlayerMatchPassingView,
    PlayerMatchShootingView,
    PlayerMatchDefendingView,
    PlayerMatchPossessionView,
    GoalkeeperMatchView,
    MatchInformationView
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

    path('api/player-passing/<int:match_id>/<str:player_name>/',
         PlayerMatchPassingView.as_view(),
         name='passing-data'),

    path('api/player-shooting/<int:match_id>/<str:player_name>/',
         PlayerMatchShootingView.as_view(),
         name='shooting-data'),

    path('api/player-defending/<int:match_id>/<str:player_name>/',
         PlayerMatchDefendingView.as_view(),
         name='defending-data'),

    path('api/player-poss/<int:match_id>/<str:player_name>/',
         PlayerMatchPossessionView.as_view(),
         name='poss-data'),

    path('api/gk/<int:match_id>/<str:player_name>/',
         GoalkeeperMatchView.as_view(),
         name='gk-data'),

     path('api/<int:match_id>/info/',
         MatchInformationView.as_view(),
         name='match-data'),
]