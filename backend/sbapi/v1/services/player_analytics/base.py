from django.db.models import Count, Q


class BaseStatsService:
    """Base class for all stats services"""
    
    def get_match_events(self, match_id, player_id):
        """Get raw events for a player in a match"""
        queryset = self.get_base_queryset(match_id, player_id)
        return self.get_events_serializer()(queryset, many=True).data

    def get_base_queryset(self, match_id, player_id):
        """Get base queryset for events"""
        raise NotImplementedError
    
    def get_events_serializer(self):
        """Get serializer for events"""
        raise NotImplementedError

