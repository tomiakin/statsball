from rest_framework import serializers
from ...base.base import BaseSerializer

class BaseEventSerializer(BaseSerializer):
    """Base serializer for common event fields"""
    team_name = serializers.CharField(source='team.name')
    player_name = serializers.CharField(source='player.name', allow_null=True)

    class Meta:
        model = None  # Set by child classes
        fields = [
            'event_id',
            'type',
            'minute',
            'second',
            'period',
            'team_name',
            'player_name',
            'x',
            'y',
            'end_x',
            'end_y',
            'outcome_type',
            'situation'
        ]