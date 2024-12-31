from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from django.shortcuts import get_object_or_404

from ..base import BaseViewSet
from ...services.player_analytics.passing import PassingStatsService

class EventsViewSet(BaseViewSet):
    """ViewSet for raw event data"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.passing_service = PassingStatsService()
        # Will add other services as needed:
        # self.shooting_service = ShootingStatsService()

    @action(detail=True, methods=['get'])
    def player_events(self, request, match_id, player_id):
        """Get all events for a player in a match"""
        try:
            events = self.passing_service.get_match_events(match_id, player_id)
            if events['status'] == 'error':
                raise NotFound(events['message'])
            
            return self.get_response(events['data'])
            
        except Exception as e:
            raise ValidationError(str(e))