from django.db import models

# Create your models here.


class Player(models.Model):
    name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class League(
        models.Model):  # add flag goals scored etc etc, date time is also wrong, # add season
    name = models.CharField(max_length=100)
    # Unique code for the league (e.g., 'PL' for Premier League)
    code = models.CharField(max_length=10, unique=True)
    # Optional league emblem URL
    emblem = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(
        max_length=50, null=True, blank=True)  # Short name for display
    crest = models.URLField()  # URL for team crest

    def __str__(self):
        return self.name


class TeamParticipation(models.Model):
    team = models.ForeignKey(
        Team, related_name='participations', on_delete=models.CASCADE)
    league = models.ForeignKey(
        League, related_name='participations', on_delete=models.CASCADE)
    position = models.IntegerField()
    playedGames = models.IntegerField()
    won = models.IntegerField()
    draw = models.IntegerField()
    lost = models.IntegerField()
    points = models.IntegerField()
    goalDifference = models.IntegerField()

    class Meta:
        # Ensures one participation record per team-league combo
        unique_together = ('team', 'league')

    def __str__(self):
        return f"{self.team.name} in {self.league.name}"


class Standings(models.Model):
    league = models.ForeignKey(
        League, related_name='standings', on_delete=models.CASCADE)  # Relation to League
    season = models.CharField(max_length=100)
    # Tracks when standings were last updated
    updated_at = models.DateTimeField(auto_now=True)
    # Relationship to team participations
    teams = models.ManyToManyField(TeamParticipation, related_name='standings')

    def __str__(self):
        return f"{self.league.name} Standings for {self.season}"
