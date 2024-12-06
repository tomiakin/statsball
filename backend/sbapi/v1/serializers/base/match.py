from rest_framework import serializers
from ....models import Match, Team, MatchPlayer, Formation
from .base import BaseSerializer, HalModelSerializer


class TeamBasicSerializer(serializers.Serializer):
    """Team serializer specifically for stats responses"""
    team_id = serializers.IntegerField()
    name = serializers.CharField()
    country = serializers.CharField()


class LineupPlayerSerializer(BaseSerializer):
    """Simplified player information for lineups"""
    name = serializers.CharField(source='player.name')

    class Meta:
        model = MatchPlayer
        fields = ['name', 'shirt_no', 'position']


class TeamLineupSerializer(serializers.Serializer):
    """Serializer for single team lineup data"""
    team = TeamBasicSerializer()
    starting_formation = serializers.CharField(allow_null=True)
    formation_changes = serializers.ListField(
        child=serializers.DictField()
    )
    starting_lineup = LineupPlayerSerializer(many=True)
    substitutions = serializers.ListField(
        child=serializers.DictField()
    )


class LineupResponseSerializer(serializers.Serializer):
    """Serializer for complete lineup response data"""
    status = serializers.CharField(default='success')
    message = serializers.CharField(allow_null=True, default=None)
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        return {
            'home_team': TeamLineupSerializer(obj['home_team']).data,
            'away_team': TeamLineupSerializer(obj['away_team']).data
        }


class MatchListSerializer(HalModelSerializer):
    """Simplified match list serializer"""
    home_team = TeamBasicSerializer()
    away_team = TeamBasicSerializer()
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = [
            'match_id',
            'start_datetime',
            'home_team',
            'away_team',
            'score',
            'venue',
            '_links'
        ]

    def get__links(self, obj):
        return {
            'self': f'/sbapi/v1/matches/{obj.match_id}',
            'lineups': f'/sbapi/v1/matches/{obj.match_id}/lineups',
            'events': f'/sbapi/v1/matches/{obj.match_id}/events'
        }


class MatchDetailSerializer(HalModelSerializer):
    """Detailed match information serializer"""
    home_team = TeamBasicSerializer()
    away_team = TeamBasicSerializer()
    competition_name = serializers.CharField(source='season.competition.name')
    season_name = serializers.CharField(source='season.name')
    _links = serializers.SerializerMethodField()

    class Meta:
        model = Match
        fields = [
            'match_id',
            'competition_name',
            'season_name',
            'start_datetime',
            'venue',
            'attendance',
            'referee_name',
            'home_team',
            'away_team',
            'home_manager_name',
            'away_manager_name',
            'home_team_average_age',
            'away_team_average_age',
            'home_score_ft',
            'away_score_ft',
            '_links'
        ]

    def get__links(self, obj):
        return {
            'self': f'/matches/{obj.match_id}',
            'lineups': f'/sbapi/v1/matches/{obj.match_id}/lineups',
            'events': f'/sbapi/v1/matches/{obj.match_id}/events',
            'stats': f'/sbapi/v1/matches/{obj.match_id}/stats'
        }
