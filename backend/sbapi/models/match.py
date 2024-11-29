from django.db import models
from django.utils import timezone

class Match(models.Model):
    match_id = models.IntegerField(primary_key=True)
    season = models.ForeignKey('sbapi.Season', on_delete=models.CASCADE)
    
    # Date/Time fields
    start_datetime = models.DateTimeField()
    venue = models.CharField(max_length=200)
    attendance = models.IntegerField(null=True)
    
    # Referee information
    referee_id = models.IntegerField(null=True)  # New field
    referee_name = models.CharField(max_length=100, null=True)  # Updated field
    
    # Team relationships
    home_team = models.ForeignKey('sbapi.Team', related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey('sbapi.Team', related_name='away_matches', on_delete=models.CASCADE)
    
    # Scores - we'll keep these at match level since they're the official record
    score = models.CharField(max_length=10)  # Raw score format e.g., "4 : 3"
    home_score_ht = models.IntegerField()
    away_score_ht = models.IntegerField()
    home_score_ft = models.IntegerField()
    away_score_ft = models.IntegerField()
    home_score_et = models.IntegerField(null=True)
    away_score_et = models.IntegerField(null=True)

    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['start_datetime']),
            models.Index(fields=['home_team']),
            models.Index(fields=['away_team']),
            models.Index(fields=['referee_id']),
            models.Index(fields=['season']),
        ]

    @property
    def competition(self):
        return self.season.competition
    
    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.start_datetime.date()})"