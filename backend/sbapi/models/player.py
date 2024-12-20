from django.db import models


class Player(models.Model):
    """Store player information"""
    player_id = models.IntegerField(primary_key=True)  # Changed to primary_key
    name = models.CharField(max_length=100)
    height = models.IntegerField(null=True)
    weight = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

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

    # Match-specific info
    shirt_no = models.IntegerField()
    position = models.CharField(max_length=20)  # e.g. 'GK'
    is_first_eleven = models.BooleanField()
    is_man_of_match = models.BooleanField(default=False)
    age = models.IntegerField()
    height = models.IntegerField(null=True)  # in cm
    weight = models.IntegerField(null=True)  # in kg

    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('match', 'player', 'team')
        indexes = [
            models.Index(fields=['position']),
            models.Index(fields=['match', 'team']),
            models.Index(fields=['is_first_eleven']),
        ]
        verbose_name = 'Match - Player Information'
        verbose_name_plural = 'Matches - Player Information'

    def __str__(self):
        return f"{self.player.name} ({self.team.name}) - Match {self.match.match_id}"

    @property
    def match_date(self):
        return self.match.start_datetime.date()
