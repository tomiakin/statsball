from django.db import models

class Event(models.Model):
    """Base model for all match events"""
    # Core identification
    id = models.BigIntegerField(primary_key=True)  # Range: [2667434829.0 to 2667506369.0]
    event_id = models.IntegerField()  # Range: [1 to 11840]
    match = models.ForeignKey('sbapi.Match', on_delete=models.CASCADE)
    team = models.ForeignKey('sbapi.Team', on_delete=models.CASCADE)
    player = models.ForeignKey('sbapi.Player', null=True, on_delete=models.CASCADE)
    player_name = models.CharField(max_length=100, null=True)
    
    # Timing
    minute = models.IntegerField()  # Range: [0 to 102]
    second = models.FloatField()  # Range: [0.0 to 59.0]
    expanded_minute = models.IntegerField()  # Range: [0 to 108]
    period = models.CharField(max_length=20)  # FirstHalf, SecondHalf
    max_minute = models.IntegerField()  # [102]
    
    # Location
    x = models.FloatField()  # Range: [0.0 to 99.6]
    y = models.FloatField()  # Range: [0.0 to 100.0]
    end_x = models.FloatField(null=True)  # Range: [0.0 to 100.0]
    end_y = models.FloatField(null=True)  # Range: [0.0 to 100.0]
    
    # Field position
    defensive_third = models.BooleanField(default=False)
    mid_third = models.BooleanField(default=False)  # Renamed from middle_third
    final_third = models.BooleanField(default=False)
    
    # Type and outcome
    type = models.CharField(max_length=50)  # Pass, Shot, etc.
    outcome_type = models.CharField(max_length=20, null=True)  # Successful, Unsuccessful
    
    # Related events/players
    related_event_id = models.FloatField(null=True)  # Changed to FloatField, Range: [63.0 to 924.0]
    related_player_id = models.FloatField(null=True)  # Changed to FloatField, Range: [22079.0 to 494120.0]
    
    # Match context
    h_a = models.CharField(max_length=1)  # 'h' or 'a'
    situation = models.CharField(max_length=50, null=True)  # OpenPlay, SetPiece, etc.
    
    # Additional data
    qualifiers = models.JSONField(default=list)
    satisfied_events_types = models.JSONField(default=list)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['match', 'minute']),
            models.Index(fields=['player', 'type']),
            models.Index(fields=['team', 'type']),
            models.Index(fields=['event_id']),
        ]