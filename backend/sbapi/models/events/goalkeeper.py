from django.db import models
from .base import Event

class GoalkeeperEvent(Event):
    """Goalkeeper-specific event details"""
    # Core actions
    is_collected = models.BooleanField(default=False)
    
    # Claims
    keeper_claim_high_lost = models.BooleanField(default=False)
    keeper_claim_high_won = models.BooleanField(default=False)
    keeper_claim_lost = models.BooleanField(default=False)
    keeper_claim_won = models.BooleanField(default=False)
    
    # Save types
    keeper_diving_save = models.BooleanField(default=False)
    keeper_missed = models.BooleanField(default=False)
    keeper_one_to_one_won = models.BooleanField(default=False)
    standing_save = models.BooleanField(default=False)
    save_feet = models.BooleanField(default=False)
    save_hands = models.BooleanField(default=False)
    
    # Save locations
    save_high_centre = models.BooleanField(default=False)
    save_high_left = models.BooleanField(default=False)
    save_high_right = models.BooleanField(default=False)
    save_low_centre = models.BooleanField(default=False)
    save_low_left = models.BooleanField(default=False)
    save_low_right = models.BooleanField(default=False)
    
    # Save zones
    save_obox = models.BooleanField(default=False)  # Outside box
    save_obp = models.BooleanField(default=False)   # Outside box proper
    save_penalty_area = models.BooleanField(default=False)
    save_six_yard_box = models.BooleanField(default=False)
    keeper_save_in_the_box = models.BooleanField(default=False)
    keeper_save_total = models.BooleanField(default=False)
    
    # Penalties
    keeper_penalty_saved = models.BooleanField(default=False)
    penalty_shootout_saved = models.BooleanField(default=False)
    penalty_shootout_saved_gk = models.BooleanField(default=False)
    penalty_shootout_conceded_gk = models.BooleanField(default=False)
    
    # Other actions
    keeper_smother = models.BooleanField(default=False)
    keeper_sweeper_lost = models.BooleanField(default=False)
    parried_danger = models.BooleanField(default=False)
    parried_safe = models.BooleanField(default=False)
    punches = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['keeper_diving_save']),
            models.Index(fields=['keeper_save_total']),
            models.Index(fields=['keeper_penalty_saved']),
        ]