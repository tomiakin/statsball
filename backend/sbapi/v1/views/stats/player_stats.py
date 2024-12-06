from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from django.shortcuts import get_object_or_404

from ..base.base import BaseViewSet
from sbapi.models import MatchPlayer, Season
from ...serializers.stats.player_stats import PlayerMatchStatsSerializer, PlayerSeasonStatsSerializer
from ...services.stats.player_stats import PlayerStatsService


class PlayerStatsViewSet(BaseViewSet):
    """ViewSet for player statistics"""
    player_stats_service = PlayerStatsService()

    @action(detail=True, methods=['get'])
    def get_match_stats(self, request, *args, **kwargs):
        """Get player stats for a specific match"""
        match_id = kwargs.get('match_id')
        player_id = kwargs.get('player_id')

        # Get event stats first
        stats_result = self.player_stats_service.calculate_match_stats(
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
            **stats_result['event_stats']['shooting'],
            **stats_result['event_stats']['passing'],
            **stats_result['event_stats']['defending']
        }

        serializer = PlayerMatchStatsSerializer(all_stats)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_season_stats(self, request, *args, **kwargs):
        """Get player stats for a season"""
        competition_id = kwargs.get('competition_id')
        season_id = kwargs.get('season_id')
        player_id = kwargs.get('player_id')

        result = self.player_stats_service.calculate_season_stats(
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
        result['stats'].update({
            'competition_name': season.competition.name,
            'season_name': season.name
        })

        serializer = PlayerSeasonStatsSerializer(data=result['stats'])
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)
