from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from django.shortcuts import get_object_or_404

from ..base.base import BaseViewSet
from sbapi.models import Season
from ...serializers.stats.team_stats import TeamMatchStatsSerializer, TeamSeasonStatsSerializer
from ...services.stats.team_stats import TeamStatsService


class TeamStatsViewSet(BaseViewSet):
    """ViewSet for team statistics"""
    team_stats_service = TeamStatsService()

    @action(detail=True, methods=['get'])
    def get_match_stats(self, request, *args, **kwargs):
        """Get team stats for a specific match"""
        match_id = kwargs.get('match_id')
        team_id = kwargs.get('team_id')
        
        result = self.team_stats_service.calculate_match_stats(match_id, team_id)
        
        if result['status'] == 'error':
            raise NotFound(result['message'])
        
        match = result['match']
        # Determine if team is home or away
        is_home = match.home_team_id == team_id
        
        match_data = {
            'team': match.home_team if is_home else match.away_team,
            'manager_name': match.home_manager_name if is_home else match.away_manager_name,
            'average_age': match.home_team_average_age if is_home else match.away_team_average_age,
            'event_stats': result['event_stats']
        }
            
        serializer = TeamMatchStatsSerializer(match_data)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_season_stats(self, request, *args, **kwargs):
        """Get team stats for a season"""
        competition_id = kwargs.get('competition_id')
        season_id = kwargs.get('season_id')
        team_id = kwargs.get('team_id')
        
        result = self.team_stats_service.calculate_season_stats(
            competition_id=competition_id,
            season_id=season_id,
            team_id=team_id
        )
        
        if result['status'] == 'error':
            raise NotFound(result['message'])
        
        # Get competition and season names
        season = get_object_or_404(Season.objects.select_related('competition'), pk=season_id)
        
        # Add competition and season info to stats
        result['stats'].update({
            'competition_name': season.competition.name,
            'season_name': season.name
        })
                
        serializer = TeamSeasonStatsSerializer(data=result['stats'])
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data)