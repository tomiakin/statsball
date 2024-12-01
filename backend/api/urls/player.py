from django.urls import path
from ..views.player.match.defending import PlayerMatchDefendingView
from ..views.player.match.goalkeeping import GoalkeeperMatchView
from ..views.player.match.passing import PlayerMatchPassingView
from ..views.player.match.possession import PlayerMatchPossessionView
from ..views.player.match.shooting import PlayerMatchShootingView
from ..views.player.match.touches import PlayerMatchTouchesView

urlpatterns = [
    path('player-match-touches/<int:match_id>/<str:player_name>/',
         PlayerMatchTouchesView.as_view(),
         name='touch-data'),

    path('player-match-passing/<int:match_id>/<str:player_name>/',
         PlayerMatchPassingView.as_view(),
         name='passing-data'),

    path('player-match-shooting/<int:match_id>/<str:player_name>/',
         PlayerMatchShootingView.as_view(),
         name='shooting-data'),

    path('player-match-def/<int:match_id>/<str:player_name>/',
         PlayerMatchDefendingView.as_view(),
         name='defending-data'),

    path('player-match-poss/<int:match_id>/<str:player_name>/',
         PlayerMatchPossessionView.as_view(),
         name='poss-data'),

    path('player-gk/<int:match_id>/<str:player_name>/',
         GoalkeeperMatchView.as_view(),
         name='gk-data'),
]
