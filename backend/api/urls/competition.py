# api/urls/competition.py
from django.urls import path
from ..views.competition.matches import CompetitionMatchesView
from ..views.competition.info import (
    CompetitionsView,
    SeasonsView,
    CompetitionInfoView,
)

urlpatterns = [
    path('competitions/',
         CompetitionsView.as_view(),
         name='competitions'),

    path('seasons/<int:competition_id>/',
         SeasonsView.as_view(),
         name='competition-seasons'),

    path('matches/<int:competition_id>/<int:season_id>/',
         CompetitionMatchesView.as_view(),
         name='competition-matches'),

    path('competition-info/<int:competition_id>/<int:season_id>/',
         CompetitionInfoView.as_view(),
         name='competition-info'),
]
