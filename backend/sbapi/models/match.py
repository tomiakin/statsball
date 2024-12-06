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
    referee_id = models.IntegerField(null=True)
    referee_name = models.CharField(max_length=100, null=True)

    # Team relationships
    home_team = models.ForeignKey(
        'sbapi.Team', related_name='home_matches', on_delete=models.CASCADE)
    away_team = models.ForeignKey(
        'sbapi.Team', related_name='away_matches', on_delete=models.CASCADE)

    # Manager information (moved from MatchTeamStats)
    home_manager_name = models.CharField(max_length=100, null=True)
    away_manager_name = models.CharField(max_length=100, null=True)

    # Team average age (moved from MatchTeamStats)
    home_team_average_age = models.FloatField(null=True)
    away_team_average_age = models.FloatField(null=True)

    # Scores
    # score = models.CharField(max_length=10)
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
        verbose_name = 'Match'
        verbose_name_plural = 'Matches'

    @property
    def competition(self):
        return self.season.competition

    @property
    def score(self):
        return f"{self.home_score_ft} : {self.away_score_ft}"

    def __str__(self):
        return f"{self.home_team} vs {self.away_team} ({self.start_datetime.date()})"
