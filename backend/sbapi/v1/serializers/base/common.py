from rest_framework import serializers


class BaseStatsSerializer(serializers.Serializer):
    """Base serializer for all stats"""
    competition_name = serializers.CharField(required=False)
    season_name = serializers.CharField(required=False)
    total_events = serializers.IntegerField(required=False)


class BasePlayerStatsSerializer(BaseStatsSerializer):
    """Base serializer for all player stats"""
    games_played = serializers.IntegerField(required=False)
    games_started = serializers.IntegerField(required=False)
    player_name = serializers.CharField()
    team_name = serializers.CharField()
    position = serializers.CharField()


class BaseTeamStatsSerializer(BaseStatsSerializer):
    """Base serializer for all team stats"""
    matches_played = serializers.IntegerField(required=False)
    team = serializers.DictField(required=False)  # For team basic info


class BaseMatchStatsSerializer(BaseStatsSerializer):
    """Base serializer for match-specific stats"""
    match_date = serializers.DateTimeField(required=False)


class BaseSeasonStatsSerializer(BaseStatsSerializer):
    """Base serializer for season aggregated stats"""
    pass
