from rest_framework import serializers
from .base import BaseEventSerializer
from sbapi.models.events import PassEvent


class PassEventSerializer(BaseEventSerializer):
    """Basic serializer for pass events - used for listings"""
    pass_type = serializers.SerializerMethodField()
    pass_accuracy = serializers.BooleanField()

    class Meta(BaseEventSerializer.Meta):
        model = PassEvent
        fields = BaseEventSerializer.Meta.fields + [
            'pass_type',
            'pass_accuracy',
            'assist',
            'pass_key',
            'big_chance_created'
        ]
    
    def get_pass_type(self, obj):
        """Simple pass type for listings"""
        if obj.pass_corner:
            return 'corner'
        elif obj.pass_cross_accurate or obj.pass_cross_inaccurate:
            return 'cross'
        elif obj.pass_freekick:
            return 'freekick'
        elif obj.pass_through_ball_accurate or obj.pass_through_ball_inaccurate:
            return 'through_ball'
        return 'regular'

class DetailedPassEventSerializer(PassEventSerializer):
    """Detailed serializer with all pass attributes"""
    assist_details = serializers.SerializerMethodField()
    key_pass_details = serializers.SerializerMethodField()
    pass_details = serializers.SerializerMethodField()
    location_stats = serializers.SerializerMethodField()

    class Meta(PassEventSerializer.Meta):
        fields = PassEventSerializer.Meta.fields + [
            'assist_details',
            'key_pass_details',
            'pass_details',
            'location_stats'
        ]

    def get_assist_details(self, obj):
        """Group assist-related attributes"""
        return {
            'is_assist': obj.assist,
            'types': {
                'corner': obj.assist_corner,
                'cross': obj.assist_cross,
                'freekick': obj.assist_freekick,
                'throughball': obj.assist_throughball,
                'throwin': obj.assist_throwin,
                'other': obj.assist_other
            },
            'intentional': obj.intentional_assist
        }

    def get_key_pass_details(self, obj):
        """Group key pass attributes"""
        return {
            'is_key_pass': obj.pass_key,
            'types': {
                'corner': obj.key_pass_corner,
                'cross': obj.key_pass_cross,
                'freekick': obj.key_pass_freekick,
                'long': obj.key_pass_long,
                'short': obj.key_pass_short,
                'throughball': obj.key_pass_throughball,
                'throwin': obj.key_pass_throwin,
                'other': obj.key_pass_other
            }
        }

    def get_pass_details(self, obj):
        """Group pass attributes"""
        return {
            'accuracy': {
                'accurate': obj.pass_accurate,
                'inaccurate': obj.pass_inaccurate
            },
            'types': {
                'corner': {
                    'attempted': obj.pass_corner,
                    'accurate': obj.pass_corner_accurate,
                    'inaccurate': obj.pass_corner_inaccurate
                },
                'cross': {
                    'accurate': obj.pass_cross_accurate,
                    'inaccurate': obj.pass_cross_inaccurate,
                    'blocked': obj.pass_cross_blocked_defensive
                },
                'freekick': {
                    'attempted': obj.pass_freekick,
                    'accurate': obj.pass_freekick_accurate,
                    'inaccurate': obj.pass_freekick_inaccurate
                },
                'long_ball': {
                    'accurate': obj.pass_long_ball_accurate,
                    'inaccurate': obj.pass_long_ball_inaccurate
                },
                'short': {
                    'accurate': obj.short_pass_accurate,
                    'inaccurate': obj.short_pass_inaccurate
                },
                'through_ball': {
                    'accurate': obj.pass_through_ball_accurate,
                    'inaccurate': obj.pass_through_ball_inaccurate
                }
            },
            'direction': {
                'forward': obj.pass_forward,
                'back': obj.pass_back,
                'left': obj.pass_left,
                'right': obj.pass_right
            },
            'body_part': {
                'head': obj.pass_head,
                'left_foot': obj.pass_left_foot,
                'right_foot': obj.pass_right_foot
            }
        }

    def get_location_stats(self, obj):
        """Location-based statistics"""
        return {
            'final_third': obj.successful_final_third_passes,
            'big_chance_created': obj.big_chance_created,
            'coordinates': {
                'start': {'x': obj.x, 'y': obj.y},
                'end': {'x': obj.end_x, 'y': obj.end_y}
            }
        }