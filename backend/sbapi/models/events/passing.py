from django.db import models
from .base import Event

class PassEvent(Event):
    """Pass-specific event details"""
    # Core pass attributes
    pass_accurate = models.BooleanField(default=False)
    pass_inaccurate = models.BooleanField(default=False)
    pass_accuracy = models.BooleanField(default=False)
    
    # Assist types
    assist = models.BooleanField(default=False)
    assist_corner = models.BooleanField(default=False)
    assist_cross = models.BooleanField(default=False)
    assist_freekick = models.BooleanField(default=False)
    assist_other = models.BooleanField(default=False)
    assist_throughball = models.BooleanField(default=False)
    assist_throwin = models.BooleanField(default=False)
    intentional_assist = models.BooleanField(default=False)
    
    # Key pass types
    key_pass_corner = models.BooleanField(default=False)
    key_pass_cross = models.BooleanField(default=False)
    key_pass_freekick = models.BooleanField(default=False)
    key_pass_long = models.BooleanField(default=False)
    key_pass_other = models.BooleanField(default=False)
    key_pass_short = models.BooleanField(default=False)
    key_pass_throughball = models.BooleanField(default=False)
    key_pass_throwin = models.BooleanField(default=False)
    pass_key = models.BooleanField(default=False)
    
    # Corner passes
    pass_corner = models.BooleanField(default=False)
    pass_corner_accurate = models.BooleanField(default=False)
    pass_corner_inaccurate = models.BooleanField(default=False)
    
    # Cross passes
    pass_cross_accurate = models.BooleanField(default=False)
    pass_cross_blocked_defensive = models.BooleanField(default=False)
    pass_cross_inaccurate = models.BooleanField(default=False)
    
    # Freekick passes
    pass_freekick = models.BooleanField(default=False)
    pass_freekick_accurate = models.BooleanField(default=False)
    pass_freekick_inaccurate = models.BooleanField(default=False)
    
    # Pass direction/zone
    pass_back = models.BooleanField(default=False)
    pass_back_zone_inaccurate = models.BooleanField(default=False)
    pass_forward = models.BooleanField(default=False)
    pass_forward_zone_accurate = models.BooleanField(default=False)
    pass_left = models.BooleanField(default=False)
    pass_right = models.BooleanField(default=False)
    
    # Pass types
    pass_chipped = models.BooleanField(default=False)
    pass_head = models.BooleanField(default=False)
    pass_left_foot = models.BooleanField(default=False)
    pass_right_foot = models.BooleanField(default=False)
    
    # Long/short passes
    pass_long_ball_accurate = models.BooleanField(default=False)
    pass_long_ball_inaccurate = models.BooleanField(default=False)
    short_pass_accurate = models.BooleanField(default=False)
    short_pass_inaccurate = models.BooleanField(default=False)
    
    # Through balls
    pass_through_ball_accurate = models.BooleanField(default=False)
    pass_through_ball_inaccurate = models.BooleanField(default=False)
    
    # Additional characteristics
    big_chance_created = models.BooleanField(default=False)
    successful_final_third_passes = models.BooleanField(default=False)
    throw_in = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['pass_accurate']),
            models.Index(fields=['assist']),
            models.Index(fields=['pass_key']),
            models.Index(fields=['big_chance_created']),
        ]