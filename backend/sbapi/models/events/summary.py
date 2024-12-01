from django.db import models
from .base import Event


class SummaryEvent(Event):
    """Summary events such as fouls, cards and substitutions"""
    # Cards
    # Yellow, Red, SecondYellow
    card_type = models.CharField(max_length=20, null=True)
    yellow_card = models.BooleanField(default=False)
    red_card = models.BooleanField(default=False)
    second_yellow = models.BooleanField(default=False)
    void_yellow_card = models.BooleanField(default=False)

    # Fouls
    foul_committed = models.BooleanField(default=False)
    # is this needed? Have opposite above
    foul_given = models.BooleanField(default=False)

    # Substitutions
    sub_on = models.BooleanField(default=False)  # Renamed from is_sub_on
    sub_off = models.BooleanField(default=False)  # Renamed from is_sub_off

    class Meta:
        db_table = 'sbapi_event_summary'  # Specific table name
        verbose_name = 'Events - Summary'
        verbose_name_plural = 'Events - Summary'
        indexes = [
            *Event.Meta.indexes,
            models.Index(fields=['card_type']),
            models.Index(fields=['foul_committed']),
            models.Index(fields=['sub_on', 'sub_off']),
        ]
