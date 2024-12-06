from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Prefetch
from django.shortcuts import get_object_or_404
from sbapi.models import Match, MatchPlayer, Formation, SummaryEvent
from ...serializers.base.match import (
    MatchListSerializer,
    MatchDetailSerializer,
    LineupResponseSerializer
)
from .base import BaseViewSet


class MatchViewSet(BaseViewSet):
    """ViewSet for managing match data."""
    lookup_field = 'match_id'
    lookup_url_kwarg = 'match_id'

    def get_serializer_class(self):
        if self.action == 'list':
            return MatchListSerializer
        return MatchDetailSerializer

    def get_queryset(self):
        """Retrieve matches with relevant data."""
        queryset = Match.objects.select_related(
            'home_team',
            'away_team',
            'season',
            'season__competition'
        )

        if self.action == 'lineups':
            queryset = queryset.prefetch_related(
                Prefetch(
                    'formation_set',
                    queryset=Formation.objects.select_related(
                        'team').order_by('start_minute')
                ),
                Prefetch(
                    'matchplayer_set',
                    queryset=MatchPlayer.objects.select_related(
                        'player', 'team')
                )
            )

        # Get query parameters
        competition_id = self.request.query_params.get('competition_id')
        season_id = self.request.query_params.get('season_id')

        if competition_id and season_id:
            queryset = queryset.filter(
                season__competition_id=competition_id,
                season_id=season_id
            )

        return queryset.order_by('-start_datetime')

    @action(detail=True, methods=['get'], url_path='lineups')
    def lineups(self, request, **kwargs):
        """Retrieve detailed lineup information."""
        match = self.get_object()

        # Retrieve formations
        home_formations = Formation.objects.filter(
            match=match,
            team=match.home_team
        ).order_by('start_minute')

        away_formations = Formation.objects.filter(
            match=match,
            team=match.away_team
        ).order_by('start_minute')

        # Retrieve starting lineups
        home_starters = MatchPlayer.objects.filter(
            match=match,
            team=match.home_team,
            is_first_eleven=True
        ).select_related('player')

        away_starters = MatchPlayer.objects.filter(
            match=match,
            team=match.away_team,
            is_first_eleven=True
        ).select_related('player')

        # Retrieve substitutions
        substitutions = (
            SummaryEvent.objects.filter(
                Q(sub_on=True) | Q(sub_off=True),
                match=match
            )
            .select_related('team')
            .order_by('minute')
        )

        # Organize substitutions by team
        home_subs = []
        away_subs = []
        for sub in substitutions:
            sub_data = {
                'minute': sub.minute,
                'player': sub.player_name,
                'type': 'on' if sub.sub_on else 'off'
            }
            if sub.team_id == match.home_team_id:
                home_subs.append(sub_data)
            else:
                away_subs.append(sub_data)

        # Prepare response data
        response_data = {
            'home_team': {
                'team': match.home_team,
                'starting_formation': home_formations.first().formation_name if home_formations else None,
                'formation_changes': [
                    {
                        'formation': f.formation_name,
                        'minute': f.start_minute
                    } for f in home_formations[1:]
                ],
                'starting_lineup': home_starters,
                'substitutions': home_subs
            },
            'away_team': {
                'team': match.away_team,
                'starting_formation': away_formations.first().formation_name if away_formations else None,
                'formation_changes': [
                    {
                        'formation': f.formation_name,
                        'minute': f.start_minute
                    } for f in away_formations[1:]
                ],
                'starting_lineup': away_starters,
                'substitutions': away_subs
            }
        }

        serializer = LineupResponseSerializer(response_data)
        return Response({
            'status': 'success',
            'data': serializer.data,
            'message': None
        })
