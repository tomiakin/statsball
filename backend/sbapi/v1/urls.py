from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.base.competition import CompetitionViewSet, CompetitionSeasonsView 
from .views.base.match import MatchViewSet
from .views.base.events import MatchEventsViewSet, EventTypeView
from .views.stats.player_stats import PlayerStatsViewSet
from .views.stats.team_stats import TeamStatsViewSet

# Create router for viewsets
router = DefaultRouter()
router.register(r'competitions', CompetitionViewSet, basename='competition')
router.register(r'matches', MatchViewSet, basename='match')

urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
    
    # Competition and season routes
    path('competitions/<int:competition_id>/seasons/', CompetitionSeasonsView.as_view()), # ALL COMPS
    path('competitions/<int:competition_id>/seasons/<int:season_id>/', include([ # ALL SEASONS OF A COMP
        path('stats/players/<int:player_id>/', 
            PlayerStatsViewSet.as_view({'get': 'get_season_stats'})), # SEASON STATS FOR A PLAYER
        path('stats/teams/<int:team_id>/', 
            TeamStatsViewSet.as_view({'get': 'get_season_stats'})), # SEASON STATS FOR A TEAM
    ])),
    
    # Match routes
    path('matches/<int:match_id>/', include([
        # Match events
        path('events/', MatchEventsViewSet.as_view({'get': 'list'})),
        path('events/stats/', MatchEventsViewSet.as_view({'get': 'stats'})),
        path('events/<str:event_type>/', EventTypeView.as_view()),
        
        # Match stats
        path('stats/', include([
            path('players/<int:player_id>/', 
                PlayerStatsViewSet.as_view({'get': 'get_match_stats'})),
            path('teams/<int:team_id>/', 
                TeamStatsViewSet.as_view({'get': 'get_match_stats'})),
        ])),
        
        # Match lineups
        path('lineups/', MatchViewSet.as_view({'get': 'lineups'})),
    ])),
]