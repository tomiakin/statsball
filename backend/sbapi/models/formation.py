from django.db import models

class Formation(models.Model):
    """Store formation information for a team in a match"""
    match = models.ForeignKey('sbapi.Match', on_delete=models.CASCADE)
    team = models.ForeignKey('sbapi.Team', on_delete=models.CASCADE)
    formation_name = models.CharField(max_length=10)  # e.g. "4231"
    captain_player_id = models.IntegerField()
    start_minute = models.IntegerField()
    end_minute = models.IntegerField()
    
    # Store player information
    player_ids = models.JSONField(default=list)
    jersey_numbers = models.JSONField(default=list)

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['formation_name']),
            models.Index(fields=['captain_player_id']),
            models.Index(fields=['match', 'team']),
        ]
        # Add uniqueness constraint for formations
        unique_together = ('match', 'team', 'start_minute', 'end_minute')
        verbose_name = 'Match Formation'
        verbose_name_plural = 'Match Formations'

    def __str__(self):
        """
        Provides a detailed string representation of the Formation instance.
        """
        match_date = self.match.start_datetime.date()
        
        # Show the formation team first, then vs their opponent
        if self.team == self.match.home_team:
            opponent = self.match.away_team.name
        else:
            opponent = self.match.home_team.name
            
        return f"{self.team.name} formation ({self.formation_name}) vs {opponent} ({match_date})"