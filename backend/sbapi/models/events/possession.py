# sbapi/models/events/possession.py
from django.db import models
from .base import Event

class PossessionEvent(Event):
    """Possession-related event details"""
    # Set pieces
    corner_awarded = models.BooleanField(default=False)
    
    # Ball control
    dispossessed = models.BooleanField(default=False)
    touches = models.BooleanField(default=False)
    turnover = models.BooleanField(default=False)
    overrun = models.BooleanField(default=False)
    is_touch = models.BooleanField(default=False)
    
    # Dribbling
    dribble_lastman = models.BooleanField(default=False)
    dribble_lost = models.BooleanField(default=False)
    dribble_won = models.BooleanField(default=False)
    
    # Fouls
    foul_committed = models.BooleanField(default=False)
    foul_given = models.BooleanField(default=False)
    penalty_won = models.BooleanField(default=False)
    
    # Offsides
    offside_given = models.BooleanField(default=False)
    offside_provoked = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['dribble_won']),
            models.Index(fields=['dispossessed']),
            models.Index(fields=['foul_committed']),
            models.Index(fields=['touches']),
        ]