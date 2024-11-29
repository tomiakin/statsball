# sbapi/models/formation.py
from django.db import models

class Formation(models.Model):
    """Store formation information for a team in a match"""
    match_team_stats = models.ForeignKey('sbapi.MatchTeamStats', on_delete=models.CASCADE)
    formation_id = models.IntegerField()
    formation_name = models.CharField(max_length=10)  # e.g. "4231"
    captain_player_id = models.IntegerField()  # Changed from FK since we just store ID
    period = models.IntegerField()  # Added from your data
    start_minute_expanded = models.IntegerField()  # Renamed to match data
    end_minute_expanded = models.IntegerField()  # Renamed to match data
    
    # Store these as JSONField since they're lists in your data
    jersey_numbers = models.JSONField(default=list)
    player_ids = models.JSONField(default=list)
    formation_slots = models.JSONField(default=list)
    formation_positions = models.JSONField(default=list)  # Contains vertical/horizontal positions

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('match_team_stats', 'formation_id', 'period')
        indexes = [
            models.Index(fields=['formation_name']),
            models.Index(fields=['captain_player_id']),
        ]

    def __str__(self):
        return f"{self.formation_name} ({self.start_minute_expanded}-{self.end_minute_expanded})"