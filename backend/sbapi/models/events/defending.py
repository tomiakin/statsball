# sbapi/models/events/defending.py
from django.db import models
from .base import Event

class DefendingEvent(Event):
    """Defensive event details"""
    # Core defensive actions
    is_tackle = models.BooleanField(default=False)
    is_interception = models.BooleanField(default=False)
    is_clearance = models.BooleanField(default=False)
    is_ball_recovery = models.BooleanField(default=False)
    
    # Aerial duels
    aerial_success = models.BooleanField(default=False)
    duel_aerial_lost = models.BooleanField(default=False)
    duel_aerial_won = models.BooleanField(default=False)
    
    # Block details
    blocked_x = models.FloatField(null=True)
    blocked_y = models.FloatField(null=True)
    
    # Clearance types
    clearance_effective = models.BooleanField(default=False)
    clearance_head = models.BooleanField(default=False)
    clearance_off_the_line = models.BooleanField(default=False)
    clearance_total = models.BooleanField(default=False)
    
    # Duels
    challenge_lost = models.BooleanField(default=False)
    defensive_duel = models.BooleanField(default=False)
    offensive_duel = models.BooleanField(default=False)
    
    # Errors
    error_leads_to_goal = models.BooleanField(default=False)
    error_leads_to_shot = models.BooleanField(default=False)
    goal_own = models.BooleanField(default=False)
    
    # Interceptions
    interception_all = models.BooleanField(default=False)
    interception_in_the_box = models.BooleanField(default=False)
    interception_won = models.BooleanField(default=False)
    
    # Blocks
    outfielder_block = models.BooleanField(default=False)
    outfielder_blocked_pass = models.BooleanField(default=False)
    six_yard_block = models.BooleanField(default=False)
    
    # Tackles
    tackle_last_man = models.BooleanField(default=False)
    tackle_lost = models.BooleanField(default=False)
    tackle_won = models.BooleanField(default=False)
    
    # Other
    penalty_conceded = models.BooleanField(default=False)

    class Meta:
        db_table = 'sbapi_event_defending'  # Specific table name
        verbose_name = 'Defending Event'
        verbose_name_plural = 'Defending Events'
        indexes = [
            *Event.Meta.indexes,  # Include parent's indexes
            models.Index(fields=['is_tackle']),
            models.Index(fields=['is_interception']),
            models.Index(fields=['is_clearance']),
            models.Index(fields=['aerial_success']),
        ]