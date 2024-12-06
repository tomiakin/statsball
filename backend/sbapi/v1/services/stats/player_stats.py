from django.db.models import Count, Avg, Sum, F, Q
from sbapi.models import MatchPlayer, Player
from sbapi.models import (
    ShootingEvent,
    PassEvent,
    DefendingEvent
)
from ..events.event_aggregator import EventAggregator

from django.db.models import Count, Avg, Sum, F, Q
from sbapi.models import MatchPlayer, Player
from ..events.event_aggregator import EventAggregator


class PlayerStatsService:
    def __init__(self):
        self.event_aggregator = EventAggregator()

    def calculate_match_stats(self, match_id, player_id):
        """Calculate detailed player stats for a specific match"""
        try:
            # Get basic match player info
            match_player = MatchPlayer.objects.get(
                match_id=match_id,
                player_id=player_id
            )

            # Get event-based stats
            event_stats = self.event_aggregator.get_player_match_events(
                match_id,
                player_id
            )

            if event_stats['status'] == 'error':
                return event_stats

            return {
                'event_stats': event_stats['stats'],
                'status': 'success'
            }

        except MatchPlayer.DoesNotExist:
            return {
                'status': 'error',
                'message': f'No stats found for player {player_id} in match {match_id}'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def calculate_season_stats(self, competition_id, season_id, player_id):
        """Calculate player stats for entire season"""
        try:
            # Get all matches for player in season
            matches = MatchPlayer.objects.filter(
                match__season__competition_id=competition_id,
                match__season_id=season_id,
                player_id=player_id
            ).select_related(
                'match',
                'player',
                'team'
            )

            if not matches.exists():
                return {
                    'status': 'error',
                    'message': f'No stats found for player {player_id} in season {season_id}'
                }

            # Get latest match for player info
            latest_match = matches.order_by('-match__start_datetime').first()
            games_played = matches.count()

            # Get event stats for all matches
            match_ids = list(matches.values_list('match_id', flat=True))

            # Initialize totals
            totals = {
                'total_shots': 0,
                'total_shots_on_target': 0,
                'total_goals': 0,
                'total_big_chances': 0,
                'total_passes': 0,
                'total_passes_completed': 0,
                'total_key_passes': 0,
                'total_assists': 0,
                'total_tackles': 0,
                'total_interceptions': 0,
                'total_ball_recoveries': 0,
                'total_duels_won': 0
            }

            # Calculate totals across all matches
            for match_id in match_ids:
                match_stats = self.event_aggregator.get_player_match_events(
                    match_id, player_id)
                if match_stats['status'] == 'success':
                    # Add shooting stats
                    shooting = match_stats['stats']['shooting']
                    totals['total_shots'] += shooting.get('shots', 0)
                    totals['total_shots_on_target'] += shooting.get(
                        'shots_on_target', 0)
                    totals['total_goals'] += shooting.get('goals', 0)
                    totals['total_big_chances'] += shooting.get(
                        'big_chances', 0)

                    # Add passing stats
                    passing = match_stats['stats']['passing']
                    totals['total_passes'] += passing.get(
                        'passes_attempted', 0)
                    totals['total_passes_completed'] += passing.get(
                        'passes_completed', 0)
                    totals['total_key_passes'] += passing.get('key_passes', 0)
                    totals['total_assists'] += passing.get('assists', 0)

                    # Add defending stats
                    defending = match_stats['stats']['defending']
                    totals['total_tackles'] += defending.get('tackles', 0)
                    totals['total_interceptions'] += defending.get(
                        'interceptions', 0)
                    totals['total_ball_recoveries'] += defending.get(
                        'ball_recoveries', 0)
                    totals['total_duels_won'] += defending.get('duels_won', 0)

            # Calculate averages
            stats = {
                # Basic info
                'player_name': latest_match.player.name,
                'team_name': latest_match.team.name,
                'position': latest_match.position,
                'games_played': games_played,
                'games_started': matches.filter(is_first_eleven=True).count(),

                # Add all totals
                **totals,

                # Calculate overall pass accuracy
                'pass_accuracy': (
                    (totals['total_passes_completed'] /
                     totals['total_passes'] * 100)
                    if totals['total_passes'] > 0 else 0
                ),

                # Calculate per game averages
                'avg_shots': totals['total_shots'] / games_played if games_played > 0 else 0,
                'avg_passes': totals['total_passes'] / games_played if games_played > 0 else 0,
                'avg_tackles': totals['total_tackles'] / games_played if games_played > 0 else 0
            }

            return {
                'status': 'success',
                'stats': stats
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }
