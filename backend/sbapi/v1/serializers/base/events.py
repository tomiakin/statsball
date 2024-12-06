from rest_framework import serializers
from ....models.events import (
    DefendingEvent,
    GoalkeeperEvent,
    PassEvent,
    PossessionEvent,
    ShootingEvent,
    SummaryEvent
)
from ..base.base import BaseSerializer


class BaseEventSerializer(BaseSerializer):
    """Base serializer for common event fields"""
    team_name = serializers.CharField(source='team.name')
    player_name = serializers.CharField(source='player.name', allow_null=True)

    class Meta:
        model = SummaryEvent
        abstract = True
        fields = [
            'event_id',
            'type',
            'minute',
            'second',
            'period',
            'team_name',
            'player_name',
            'x',
            'y',
            'end_x',
            'end_y',
            'outcome_type',
            'situation'
        ]


class DefendingEventSerializer(BaseEventSerializer):
    class Meta(BaseEventSerializer.Meta):
        model = DefendingEvent
        fields = BaseEventSerializer.Meta.fields + [
            'is_tackle',
            'is_interception',
            'is_clearance',
            'is_ball_recovery',
            'aerial_success',
            'clearance_effective',
            'tackle_won',
            'interception_won',
            'defensive_duel',
            'error_leads_to_goal',
            'error_leads_to_shot',
        ]


class GoalkeeperEventSerializer(BaseEventSerializer):
    class Meta(BaseEventSerializer.Meta):
        model = GoalkeeperEvent
        fields = BaseEventSerializer.Meta.fields + [
            'keeper_save_total',
            'keeper_claim_won',
            'keeper_claim_lost',
            'keeper_diving_save',
            'keeper_save_in_the_box',
            'keeper_penalty_saved',
            'save_high_centre',
            'save_high_left',
            'save_high_right',
            'save_low_centre',
            'save_low_left',
            'save_low_right',
        ]


class PassEventSerializer(BaseEventSerializer):
    class Meta(BaseEventSerializer.Meta):
        model = PassEvent
        fields = BaseEventSerializer.Meta.fields + [
            'pass_accurate',
            'pass_inaccurate',
            'assist',
            'key_pass_cross',
            'key_pass_throughball',
            'pass_cross_accurate',
            'pass_through_ball_accurate',
            'big_chance_created',
            'successful_final_third_passes',
        ]


class PossessionEventSerializer(BaseEventSerializer):
    class Meta(BaseEventSerializer.Meta):
        model = PossessionEvent
        fields = BaseEventSerializer.Meta.fields + [
            'dispossessed',
            'touches',
            'dribble_won',
            'dribble_lost',
            'penalty_won',
            'offside_given',
        ]


class ShootingEventSerializer(BaseEventSerializer):
    class Meta(BaseEventSerializer.Meta):
        model = ShootingEvent
        fields = BaseEventSerializer.Meta.fields + [
            'is_goal',
            'is_shot',
            'shot_on_target',
            'big_chance_scored',
            'big_chance_missed',
            'goal_mouth_y',
            'goal_mouth_z',
            'shot_body_type',
            'shot_penalty_area',
            'shot_six_yard_box',
        ]


class SummaryEventSerializer(BaseEventSerializer):
    class Meta(BaseEventSerializer.Meta):
        model = SummaryEvent
        fields = BaseEventSerializer.Meta.fields + [
            'card_type',
            'yellow_card',
            'red_card',
            'second_yellow',
            'foul_committed',
            'sub_on',
            'sub_off',
        ]


# Factory function to get appropriate serializer
EVENT_TYPE_SERIALIZERS = {
    'defending': DefendingEventSerializer,
    'goalkeeper': GoalkeeperEventSerializer,
    'passing': PassEventSerializer,
    'possession': PossessionEventSerializer,
    'shooting': ShootingEventSerializer,
    'summary': SummaryEventSerializer,
}


def get_event_serializer(event_type):
    """Returns appropriate serializer based on event type"""
    return EVENT_TYPE_SERIALIZERS.get(event_type, BaseEventSerializer)
