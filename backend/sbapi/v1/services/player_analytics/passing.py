# services/stats.py
from django.db.models import Count, Q
from sbapi.models.events import PassEvent
from ...serializers.match_events.passing import DetailedPassEventSerializer
from .base import BaseStatsService

class PassingStatsService(BaseStatsService):
    """Service for calculating passing statistics"""
    
    def get_base_queryset(self, match_id, player_id):
        return PassEvent.objects.filter(
            match_id=match_id,
            player_id=player_id
        ).select_related('team', 'player')
    
    def get_events_serializer(self):
        return DetailedPassEventSerializer
    
    def get_player_match_stats(self, match_id, player_id):
        """Get aggregated pass stats for a match"""
        try:
            queryset = self.get_base_queryset(match_id, player_id)
            
            if not queryset.exists():
                return {
                    'status': 'error',
                    'message': f'No passing events found for player {player_id} in match {match_id}'
                }
            
            # Calculate basic stats
            basic_stats = queryset.aggregate(
                total_passes=Count('id'),
                accurate_passes=Count('id', filter=Q(pass_accurate=True)),
                assists=Count('id', filter=Q(assist=True)),
                key_passes=Count('id', filter=Q(pass_key=True)),
                big_chances=Count('id', filter=Q(big_chance_created=True))
            )
            
            # Pass types
            pass_types = queryset.aggregate(
                corners=Count('id', filter=Q(pass_corner=True)),
                crosses_accurate=Count('id', filter=Q(pass_cross_accurate=True)),
                crosses_inaccurate=Count('id', filter=Q(pass_cross_inaccurate=True)),
                through_balls_accurate=Count('id', filter=Q(pass_through_ball_accurate=True)),
                through_balls_inaccurate=Count('id', filter=Q(pass_through_ball_inaccurate=True))
            )
            
            # Calculate percentages
            total_passes = basic_stats['total_passes']
            
            return {
                'status': 'success',
                'stats': {
                    'basic': {
                        'total_passes': total_passes,
                        'accurate_passes': basic_stats['accurate_passes'],
                        'pass_accuracy': self._calculate_percentage(
                            basic_stats['accurate_passes'], 
                            total_passes
                        ),
                        'assists': basic_stats['assists'],
                        'key_passes': basic_stats['key_passes'],
                        'big_chances_created': basic_stats['big_chances']
                    },
                    'types': {
                        'corners': pass_types['corners'],
                        'crosses': {
                            'total': pass_types['crosses_accurate'] + pass_types['crosses_inaccurate'],
                            'accurate': pass_types['crosses_accurate'],
                            'accuracy': self._calculate_percentage(
                                pass_types['crosses_accurate'],
                                pass_types['crosses_accurate'] + pass_types['crosses_inaccurate']
                            )
                        },
                        'through_balls': {
                            'total': pass_types['through_balls_accurate'] + pass_types['through_balls_inaccurate'],
                            'accurate': pass_types['through_balls_accurate'],
                            'accuracy': self._calculate_percentage(
                                pass_types['through_balls_accurate'],
                                pass_types['through_balls_accurate'] + pass_types['through_balls_inaccurate']
                            )
                        }
                    }
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def get_player_season_stats(self, competition_id, season_id, player_id):
        """Get season aggregated stats"""
        try:
            from sbapi.models import Match
            
            # Get all matches for the player in this season
            matches = Match.objects.filter(
                season__competition_id=competition_id,
                season_id=season_id,
                matchplayer__player_id=player_id
            ).values_list('id', flat=True)
            
            if not matches:
                return {
                    'status': 'error',
                    'message': f'No matches found for player {player_id} in season {season_id}'
                }
            
            # Get all passing events for these matches
            events = PassEvent.objects.filter(
                match_id__in=matches,
                player_id=player_id
            )
            
            # Calculate totals
            totals = events.aggregate(
                total_passes=Count('id'),
                accurate_passes=Count('id', filter=Q(pass_accurate=True)),
                assists=Count('id', filter=Q(assist=True)),
                key_passes=Count('id', filter=Q(pass_key=True)),
                big_chances=Count('id', filter=Q(big_chance_created=True))
            )
            
            matches_played = len(matches)
            
            return {
                'status': 'success',
                'stats': {
                    'matches_played': matches_played,
                    'totals': {
                        'passes': totals['total_passes'],
                        'accurate_passes': totals['accurate_passes'],
                        'pass_accuracy': self._calculate_percentage(
                            totals['accurate_passes'],
                            totals['total_passes']
                        ),
                        'assists': totals['assists'],
                        'key_passes': totals['key_passes'],
                        'big_chances_created': totals['big_chances']
                    },
                    'per_90': {
                        'passes': self._calculate_per_90(
                            totals['total_passes'], 
                            matches_played
                        ),
                        'key_passes': self._calculate_per_90(
                            totals['key_passes'],
                            matches_played
                        ),
                        'assists': self._calculate_per_90(
                            totals['assists'],
                            matches_played
                        )
                    }
                }
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
    
    def _calculate_percentage(self, part, total):
        """Calculate percentage with zero handling"""
        return round((part / total * 100) if total > 0 else 0, 2)
    
    def _calculate_per_90(self, value, matches):
        """Calculate per 90 minutes value"""
        return round((value / matches) * 90, 2)