# sbapi/models/formation.py
from django.db import models


class Formation(models.Model):
    """Store formation information for a team in a match"""
    match_team_stats = models.ForeignKey(
        'sbapi.MatchTeamStats', on_delete=models.CASCADE)
    formation_id = models.IntegerField()
    formation_name = models.CharField(max_length=10)  # e.g. "4231"
    # Changed from FK since we just store ID
    captain_player_id = models.IntegerField()
    period = models.IntegerField()  # Added from your data
    start_minute_expanded = models.IntegerField()  # Renamed to match data
    end_minute_expanded = models.IntegerField()  # Renamed to match data

    # Store these as JSONField since they're lists in data
    jersey_numbers = models.JSONField(default=list)
    player_ids = models.JSONField(default=list)
    formation_slots = models.JSONField(default=list)
    # Contains vertical/horizontal positions
    formation_positions = models.JSONField(default=list)

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('match_team_stats', 'formation_id', 'period')
        indexes = [
            models.Index(fields=['formation_name']),
            models.Index(fields=['captain_player_id']),
        ]
        verbose_name = 'Match - Formations'
        verbose_name_plural = 'Matches - Formations'

    def __str__(self):
        return f"{self.formation_name} ({self.start_minute_expanded}-{self.end_minute_expanded})"
