from django.db import models
from .base import Event

class SummaryEvent(Event):
    """Summary events like cards and substitutions"""
    # Cards
    card_type = models.CharField(max_length=20, null=True)  # Yellow, Red, SecondYellow
    yellow_card = models.BooleanField(default=False)
    red_card = models.BooleanField(default=False)
    second_yellow = models.BooleanField(default=False)
    void_yellow_card = models.BooleanField(default=False)
    
    # Substitutions
    sub_on = models.BooleanField(default=False)  # Renamed from is_sub_on
    sub_off = models.BooleanField(default=False)  # Renamed from is_sub_off
    
    class Meta:
        indexes = [
            models.Index(fields=['card_type']),
            models.Index(fields=['sub_on', 'sub_off']),
        ]