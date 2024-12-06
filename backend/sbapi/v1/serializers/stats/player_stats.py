from rest_framework import serializers
from ..base.common import BaseMatchStatsSerializer, BaseSeasonStatsSerializer, BasePlayerStatsSerializer


class PlayerMatchStatsSerializer(
        BaseMatchStatsSerializer, BasePlayerStatsSerializer):
    """Detailed stats for a player in a specific match"""
    # Basic info
    player_name = serializers.CharField()
    team_name = serializers.CharField()
    # Changed from DateField to DateTimeField to match match.start_datetime
    match_date = serializers.DateTimeField()
    position = serializers.CharField()
    shirt_no = serializers.IntegerField()
    is_first_eleven = serializers.BooleanField()

    # Shooting stats
    shots = serializers.IntegerField(default=0)
    shots_on_target = serializers.IntegerField(default=0)
    goals = serializers.IntegerField(default=0)
    big_chances = serializers.IntegerField(default=0)

    # Passing stats
    passes_attempted = serializers.IntegerField(default=0)
    passes_completed = serializers.IntegerField(default=0)
    pass_accuracy = serializers.FloatField(default=0.0)
    key_passes = serializers.IntegerField(default=0)
    assists = serializers.IntegerField(default=0)

    # Defending stats
    tackles = serializers.IntegerField(default=0)
    interceptions = serializers.IntegerField(default=0)
    ball_recoveries = serializers.IntegerField(default=0)
    duels_won = serializers.IntegerField(default=0)


class PlayerSeasonStatsSerializer(
        BaseSeasonStatsSerializer, BasePlayerStatsSerializer):
    """Season stats serializer"""
    # Basic info
    player_name = serializers.CharField()
    team_name = serializers.CharField()
    position = serializers.CharField()
    games_played = serializers.IntegerField()
    games_started = serializers.IntegerField()

    # Aggregated shooting stats
    total_shots = serializers.IntegerField(default=0)
    total_shots_on_target = serializers.IntegerField(default=0)
    total_goals = serializers.IntegerField(default=0)
    total_big_chances = serializers.IntegerField(default=0)

    # Aggregated passing stats
    total_passes = serializers.IntegerField(default=0)
    total_passes_completed = serializers.IntegerField(default=0)
    pass_accuracy = serializers.FloatField(default=0.0)
    total_key_passes = serializers.IntegerField(default=0)
    total_assists = serializers.IntegerField(default=0)

    # Aggregated defending stats
    total_tackles = serializers.IntegerField(default=0)
    total_interceptions = serializers.IntegerField(default=0)
    total_ball_recoveries = serializers.IntegerField(default=0)
    total_duels_won = serializers.IntegerField(default=0)

    # Per game averages
    avg_shots = serializers.FloatField(default=0.0)
    avg_passes = serializers.FloatField(default=0.0)
    avg_tackles = serializers.FloatField(default=0.0)
