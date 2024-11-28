from django.db import models

class MatchTeamStats(models.Model):
    """Store team statistics for a specific match"""
    match = models.ForeignKey('sbapi.Match', on_delete=models.CASCADE)
    team = models.ForeignKey('sbapi.Team', on_delete=models.CASCADE)
    is_home = models.BooleanField()
    
    # Team info from your data
    field = models.CharField(max_length=10)  # home/away
    average_age = models.FloatField()
    manager_name = models.CharField(max_length=100)
    country_name = models.CharField(max_length=100)

    # Scores
    running_score = models.IntegerField()
    
    # Team stats stored as JSON
    stats = models.JSONField(default=dict, help_text="""
    Stores team statistics by minute including:
    - minutesWithStats
    - ratings
    - shots metrics
    - possession metrics
    - passing metrics
    - aerial metrics
    - corners metrics
    - throw-ins metrics
    And other match statistics
    """)

    class Meta:
        unique_together = ('match', 'team')
        verbose_name = 'Match team statistic'
        verbose_name_plural = 'Match team statistics'

    def __str__(self):
        team_name = self.team.name 
        match_date = self.match.start_datetime.date()
        return f"{team_name} stats vs {self.match.home_team.name if not self.is_home else self.match.away_team.name} ({match_date})"