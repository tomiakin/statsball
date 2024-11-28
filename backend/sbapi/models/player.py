from django.db import models

class Player(models.Model):
    """Store player information"""
    player_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    height = models.IntegerField(null=True)  # in cm
    weight = models.IntegerField(null=True)  # in kg
    
    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return self.name

class MatchPlayer(models.Model):
    """Store player information specific to a match"""
    match = models.ForeignKey('sbapi.Match', on_delete=models.CASCADE)
    player = models.ForeignKey('sbapi.Player', on_delete=models.CASCADE)
    team = models.ForeignKey('sbapi.Team', on_delete=models.CASCADE)
    
    # Match-specific info from your data
    shirt_no = models.IntegerField()  # Renamed to match data
    position = models.CharField(max_length=20)  # e.g. 'GK'
    field = models.CharField(max_length=10)  # home/away
    is_first_eleven = models.BooleanField()
    is_man_of_match = models.BooleanField()
    age = models.IntegerField()
    height = models.IntegerField()  # in cm
    weight = models.IntegerField()  # in kg

    # Statistics from your data
    stats = models.JSONField(default=dict)  # Stores various player stats by minute

    class Meta:
        unique_together = ('match', 'player', 'team')
        indexes = [
            models.Index(fields=['position']),
        ]

    def __str__(self):
        return f"{self.player.name} ({self.team.name}) - Match {self.match.match_id}"