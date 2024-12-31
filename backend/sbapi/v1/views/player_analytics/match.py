from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from django.shortcuts import get_object_or_404

from ..base.base import BaseViewSet
from sbapi.models import MatchPlayer, Season
from ...services.player_analytics.passing import PassingStatsService

class PlayerStatsViewSet(BaseViewSet):
    """ViewSet for player statistics"""
    passing_stats_service = PassingStatsService()
    # Add other services as needed:
    # shooting_stats_service = ShootingStatsService()
    
    @action(detail=True, methods=['get'])
    def match_stats(self, request, *args, **kwargs):
        """Get player stats for a specific match"""
        match_id = kwargs.get('match_id')
        player_id = kwargs.get('player_id')

        # Get event stats first
        stats_result = self.passing_stats_service.get_player_match_stats(
            match_id, player_id)

        if stats_result['status'] == 'error':
            raise NotFound(stats_result['message'])

        # Get match player info
        match_player = get_object_or_404(
            MatchPlayer.objects.select_related('player', 'team', 'match'),
            match_id=match_id,
            player_id=player_id
        )

        # Create data dictionary combining match player info and event stats
        all_stats = {
            'player_name': match_player.player.name,
            'team_name': match_player.team.name,
            'match_date': match_player.match.start_datetime,
            'position': match_player.position,
            'shirt_no': match_player.shirt_no,
            'is_first_eleven': match_player.is_first_eleven,
            'passing': stats_result['stats']
            # Add other event types as you create them:
            # 'shooting': shooting_result['stats']
        }

        return self.get_response(all_stats)

    @action(detail=True, methods=['get'])
    def season_stats(self, request, *args, **kwargs):
        """Get player stats for a season"""
        competition_id = kwargs.get('competition_id')
        season_id = kwargs.get('season_id')
        player_id = kwargs.get('player_id')

        result = self.passing_stats_service.get_player_season_stats(
            competition_id,
            season_id,
            player_id
        )

        if result['status'] == 'error':
            raise NotFound(result['message'])

        # Get competition and season names
        season = get_object_or_404(
            Season.objects.select_related('competition'),
            pk=season_id)

        # Add competition and season info to stats
        stats_data = {
            'competition_name': season.competition.name,
            'season_name': season.name,
            'passing': result['stats']
            # Add other event types as you create them:
            # 'shooting': shooting_result['stats']
        }

        return self.get_response(stats_data)