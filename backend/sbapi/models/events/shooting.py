from django.db import models
from .base import Event

class ShootingEvent(Event):
    """Shot-specific event details"""
    # Big chances
    big_chance_missed = models.BooleanField(default=False)
    big_chance_scored = models.BooleanField(default=False)
    
    # Close misses
    close_miss_high = models.BooleanField(default=False)
    close_miss_high_left = models.BooleanField(default=False)
    close_miss_high_right = models.BooleanField(default=False)
    close_miss_left = models.BooleanField(default=False)
    close_miss_right = models.BooleanField(default=False)
    
    # Goals
    is_goal = models.BooleanField(default=False)
    goal_counter = models.BooleanField(default=False)
    goal_head = models.BooleanField(default=False)
    goal_left_foot = models.BooleanField(default=False)
    goal_right_foot = models.BooleanField(default=False)
    goal_normal = models.BooleanField(default=False)
    goal_open_play = models.BooleanField(default=False)
    goal_set_piece = models.BooleanField(default=False)
    
    # Goal location
    goal_obox = models.BooleanField(default=False)
    goal_obp = models.BooleanField(default=False)
    goal_penalty_area = models.BooleanField(default=False)
    goal_six_yard_box = models.BooleanField(default=False)
    goal_mouth_y = models.FloatField(null=True)  # Range: 7.1 to 93.4
    goal_mouth_z = models.FloatField(null=True)  # Range: 1.3 to 86.1
    
    # Shot flags
    is_shot = models.BooleanField(default=False)
    shot_blocked = models.BooleanField(default=False)
    shot_counter = models.BooleanField(default=False)
    shot_direct_corner = models.BooleanField(default=False)
    shot_on_post = models.BooleanField(default=False)
    shot_on_target = models.BooleanField(default=False)
    shot_off_target = models.BooleanField(default=False)
    shot_off_target_inside_box = models.BooleanField(default=False)
    shots_total = models.BooleanField(default=False)
    
    # Shot body part
    shot_body_type = models.CharField(max_length=20, null=True)
    shot_head = models.BooleanField(default=False)
    shot_left_foot = models.BooleanField(default=False)
    shot_right_foot = models.BooleanField(default=False)
    
    # Shot location
    shot_obox_total = models.BooleanField(default=False)
    shot_obp = models.BooleanField(default=False)
    shot_penalty_area = models.BooleanField(default=False)
    shot_six_yard_box = models.BooleanField(default=False)
    
    # Shot type
    shot_open_play = models.BooleanField(default=False)
    shot_set_piece = models.BooleanField(default=False)
    
    # Penalties
    penalty_missed = models.BooleanField(default=False)
    penalty_scored = models.BooleanField(default=False)
    penalty_shootout_missed_off_target = models.BooleanField(default=False)
    penalty_shootout_scored = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['is_goal']),
            models.Index(fields=['is_shot']),
            models.Index(fields=['shot_on_target']),
            models.Index(fields=['big_chance_scored']),
        ]