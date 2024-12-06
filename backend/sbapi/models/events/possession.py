# sbapi/models/events/possession.py
from django.db import models
from .base import Event


class PossessionEvent(Event):
    """Possession-related event details"""
    # Set pieces
    corner_awarded = models.BooleanField(default=False) # recorded as h/a for conceded/won

    # Ball control
    dispossessed = models.BooleanField(default=False)
    turnover = models.BooleanField(default=False)
    overrun = models.BooleanField(default=False)

    # Dribbling
    dribble_lastman = models.BooleanField(default=False)
    dribble_lost = models.BooleanField(default=False)
    dribble_won = models.BooleanField(default=False)

    class Meta:
        db_table = 'sbapi_event_possession'  # Specific table name
        verbose_name = 'Events - Possession'
        verbose_name_plural = 'Events - Possession'
        indexes = [
            *Event.Meta.indexes,
            models.Index(fields=['dribble_won']),
            models.Index(fields=['dispossessed']),
            models.Index(fields=['touches']),
        ]
