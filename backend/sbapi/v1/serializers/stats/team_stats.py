from rest_framework import serializers
from ..base.match import TeamBasicSerializer
from ..base.common import BaseMatchStatsSerializer, BaseSeasonStatsSerializer, BaseTeamStatsSerializer


class TeamMatchStatsSerializer(
        BaseMatchStatsSerializer, BaseTeamStatsSerializer):
    """Team statistics for a specific match"""
    team = TeamBasicSerializer()
    manager_name = serializers.CharField()
    average_age = serializers.FloatField()

    # Event stats from 'possession' category
    possession = serializers.FloatField(
        source='event_stats.possession.possession_pct', default=0)
    touches = serializers.IntegerField(
        source='event_stats.possession.touches', default=0)
    possession_lost = serializers.IntegerField(
        source='event_stats.possession.possession_lost', default=0)

    # Event stats from 'shooting' category
    total_shots = serializers.IntegerField(
        source='event_stats.shooting.total_shots', default=0)
    shots_on_target = serializers.IntegerField(
        source='event_stats.shooting.shots_on_target', default=0)
    goals = serializers.IntegerField(
        source='event_stats.shooting.goals', default=0)
    big_chances = serializers.IntegerField(
        source='event_stats.shooting.big_chances', default=0)

    # Event stats from 'passing' category
    total_passes = serializers.IntegerField(
        source='event_stats.passing.total_passes', default=0)
    accurate_passes = serializers.IntegerField(
        source='event_stats.passing.accurate_passes', default=0)
    key_passes = serializers.IntegerField(
        source='event_stats.passing.key_passes', default=0)
    assists = serializers.IntegerField(
        source='event_stats.passing.assists', default=0)

    # Event stats from 'defending' category
    tackles_won = serializers.IntegerField(
        source='event_stats.defending.tackles_won', default=0)
    interceptions = serializers.IntegerField(
        source='event_stats.defending.interceptions', default=0)
    clearances = serializers.IntegerField(
        source='event_stats.defending.clearances', default=0)
    blocks = serializers.IntegerField(
        source='event_stats.defending.blocks', default=0)


class TeamSeasonStatsSerializer(
        BaseSeasonStatsSerializer, BaseTeamStatsSerializer):
    """Team statistics aggregated over a season"""
    team = TeamBasicSerializer()
    matches_played = serializers.IntegerField()
    goals_for = serializers.IntegerField()
    avg_possession = serializers.FloatField()
    avg_age = serializers.FloatField(allow_null=True)
    home_matches = serializers.IntegerField()
    away_matches = serializers.IntegerField()
    manager = serializers.CharField()
    formation = serializers.CharField()
