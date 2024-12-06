from django.db import models


class Event(models.Model):
    """Base model for all match events, these fields are informative"""
    # Core identification
    id = models.AutoField(primary_key=True)  # Django's auto-incrementing primary key
    source_id = models.BigIntegerField()     # The original DataFrame id (2.755319e+09)
    event_id = models.IntegerField()         # The original eventId that groups related actions (21, 22, etc)
    match = models.ForeignKey('sbapi.Match', on_delete=models.CASCADE)
    team = models.ForeignKey('sbapi.Team', on_delete=models.CASCADE)
    player = models.ForeignKey(
        'sbapi.Player', null=True, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=100, null=True)

    # Timing
    minute = models.IntegerField()  # Range: [0 to 102]
    second = models.FloatField(null=True)  # Range: [0.0 to 59.0]
    expanded_minute = models.IntegerField()  # Range: [0 to 108]
    period = models.CharField(max_length=20)  # FirstHalf, SecondHalf, PenaltyShootout, FirstPeriodOfExtraTime, SecondPeriodOfExtraTime
    max_minute = models.IntegerField()  # [102]

    # Location
    x = models.FloatField()  # Range: [0.0 to 100]
    y = models.FloatField()  # Range: [0.0 to 100.0]
    end_x = models.FloatField(null=True)  # Range: [0.0 to 100.0]
    end_y = models.FloatField(null=True)  # Range: [0.0 to 100.0]

    # Did this event involve a touch?
    is_touch = models.BooleanField(default=False)
    touches = models.BooleanField(default=False)

    # Field position
    defensive_third = models.BooleanField(default=False)
    mid_third = models.BooleanField(default=False)
    final_third = models.BooleanField(default=False)

    # Type and outcome
    type = models.CharField(max_length=50)  # Pass, Shot, etc. (see type in docs/)
    outcome_type = models.CharField(
        max_length=20, null=True)  # Successful, Unsuccessful

    # Related events/players
    # Changed to FloatField, Range: [63.0 to 924.0]
    related_event_id = models.FloatField(null=True)
    # Changed to FloatField, Range: [22079.0 to 494120.0]
    related_player_id = models.FloatField(null=True)

    # Match context
    h_a = models.CharField(max_length=1)  # 'h' or 'a'
    
    # OpenPlay, SetPiece, etc.
    situation = models.CharField(max_length=50, null=True)
    """Regular an attempt created from an open-play attack.
Set-piece  an attempt created where the ball starts from an indirect free-kick dead-ball situation.
Throw-in  an attempt created from a throw-in.
Direct free-kick  an attempt at goal directly from free-kick situation.
Direct corner  a goal scored directly from a corner by the corner-taker, or an attempt created from a corner situation.
Fast break  an attempt created after a team quickly turn defence into attack, winning the ball in their own half (counter-attack).
Penalty  The penalty attempt itself, any follow-up shot would be classed as a set-piece attempt. Passed penalties are also counted as penalty pattern of play"""

    # Additional data
    qualifiers = models.JSONField(default=list)
    satisfied_events_types = models.JSONField(default=list)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['match', 'minute']),
            models.Index(fields=['player', 'type']),
            models.Index(fields=['team', 'type']),
            models.Index(fields=['event_id']),  # Meaningful for finding related actions
            models.Index(fields=['source_id']),  # Index for the original DataFrame id
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['match', 'source_id'],
                name='%(app_label)s_%(class)s_unique_match_source'
            )
        ]

#   # Aerial (Type) duels (won and lost are the same, just opposite)
    # looks empty (ie no/null for evryone so may need to do aerial_success + duel OR use the type (Aerial + outomce column)
    # carries xG and xA need calculating