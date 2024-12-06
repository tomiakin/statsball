from django.db import models
from .base import Event


class DefendingEvent(Event):
    """
    Model representing defensive actions in football/soccer matches.
    Inherits from base Event model.

    This model tracks various defensive actions including tackles, interceptions,
    clearances, aerial duels, and defensive errors.
    """

    # Core defensive actions
    is_tackle = models.BooleanField(
        default=False,
        help_text="Quick identifier for tackle events"
    )
    is_interception = models.BooleanField(
        default=False,
        help_text="Quick identifier for interception events. Occurs when a player reads and "
        "intercepts an opponent's pass by moving into the line of the intended pass"
    )
    is_clearance = models.BooleanField(
        default=False,
        help_text="Quick identifier for clearance events. Represents an action where "
        "a player attempts to get the ball away from a dangerous zone"
    )
    is_ball_recovery = models.BooleanField(
        default=False,
        help_text="Quick identifier for ball recovery events. Occurs when a player recovers "
        "the ball in a situation where neither team has possession"
    )

    # Aerial duels
    aerial_success = models.BooleanField(
        default=False,
        help_text="Indicates successful aerial duel"
    )
    duel_aerial_lost = models.BooleanField(
        default=False,
        help_text="Indicates lost aerial duel"
    )
    duel_aerial_won = models.BooleanField(
        default=False,
        help_text="Indicates won aerial duel"
    )

    # Block coordinates
    blocked_x = models.FloatField(
        null=True,
        help_text="X-coordinate of block location"
    )
    blocked_y = models.FloatField(
        null=True,
        help_text="Y-coordinate of block location"
    )

    # Clearance types
    clearance_effective = models.BooleanField(
        default=False,
        help_text="Indicates if the clearance was effective"
    )
    clearance_head = models.BooleanField(
        default=False,
        help_text="Indicates if the clearance was made with the head"
    )
    clearance_off_the_line = models.BooleanField(
        default=False,
        help_text="Indicates if the clearance was made off the goal line"
    )
    clearance_total = models.BooleanField(
        default=False,
        help_text="Total clearance indicator (purpose needs clarification)"
    )

    # Duels and challenges
    challenge_lost = models.BooleanField(
        default=False,
        help_text="Indicates when a player is dribbled past and fails to win the ball"
    )
    defensive_duel = models.BooleanField(
        default=False,
        help_text="Indicates involvement in a defensive duel"
    )
    offensive_duel = models.BooleanField(
        default=False,
        help_text="Indicates involvement in an offensive duel"
    )

    # Defensive errors
    error_leads_to_goal = models.BooleanField(
        default=False,
        help_text="Indicates if a defensive error led to a goal"
    )
    error_leads_to_shot = models.BooleanField(
        default=False,
        help_text="Indicates if a defensive error led to a shot"
    )
    goal_own = models.BooleanField(
        default=False,
        help_text="Indicates if an own goal was scored"
    )

    # Interception details
    interception_all = models.BooleanField(
        default=False,
        help_text="Indicates any type of interception"
    )
    interception_in_the_box = models.BooleanField(
        default=False,
        help_text="Indicates interception made inside the penalty box"
    )
    interception_won = models.BooleanField(
        default=False,
        help_text="Indicates successful interception"
    )

    # Block types
    outfielder_block = models.BooleanField(
        default=False,
        help_text="Indicates block made by an outfield player (for shots?)"
    )
    outfielder_blocked_pass = models.BooleanField(
        default=False,
        help_text="Indicates blocked pass by an outfield player. Similar to interception "
        "but with less reading of the pass"
    )
    six_yard_block = models.BooleanField(
        default=False,
        help_text="Indicates block made in the six-yard box"
    )

    # Tackle outcomes
    tackle_last_man = models.BooleanField(
        default=False,
        help_text="Indicates tackle made as the last defending player"
    )
    tackle_lost = models.BooleanField(
        default=False,
        help_text="Indicates tackle where the ball goes to an opposition player"
    )
    tackle_won = models.BooleanField(
        default=False,
        help_text="Indicates tackle where the tackler or teammate regains possession, "
        "or the ball goes safely out of play"
    )

    class Meta:
        db_table = 'sbapi_event_defending'
        verbose_name = 'Events - Defending'
        verbose_name_plural = 'Events - Defending'
        indexes = [
            *Event.Meta.indexes,  # Include parent's indexes
            models.Index(fields=['is_tackle']),
            models.Index(fields=['is_interception']),
            models.Index(fields=['is_clearance']),
            models.Index(fields=['aerial_success']),
        ]
