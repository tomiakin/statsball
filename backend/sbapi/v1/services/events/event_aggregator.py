from django.db.models import Count, Q, Sum, F
from sbapi.models.events import (
    ShootingEvent,
    PassEvent,
    DefendingEvent,
    GoalkeeperEvent,
    PossessionEvent
)


class EventAggregator:
    """Service for aggregating and calculating event statistics"""

    def get_match_events(self, match_id, event_type=None):
        """Get events for a match with optional type filtering"""
        try:
            event_mapping = {
                'shooting': ShootingEvent,
                'passing': PassEvent,
                'defending': DefendingEvent,
                'goalkeeper': GoalkeeperEvent,
                'possession': PossessionEvent
            }

            if event_type:
                if event_type not in event_mapping:
                    return {'status': 'error', 'message': 'Invalid event type'}

                events = event_mapping[event_type].objects.filter(
                    match_id=match_id
                ).select_related('team', 'player')

                return {
                    'events': events,
                    'count': events.count(),
                    'status': 'success'
                }

            # If no type specified, return counts for each type
            return {
                'counts': {
                    event_type: model.objects.filter(
                        match_id=match_id
                    ).count()
                    for event_type, model in event_mapping.items()
                },
                'status': 'success'
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_team_match_events(self, match_id, team_id):
        """Aggregate all events for a team in a match"""
        try:
            event_stats = {
                'possession': self._get_possession_stats(match_id, team_id),
                'shooting': self._get_shooting_stats(match_id, team_id),
                'passing': self._get_passing_stats(match_id, team_id),
                'defending': self._get_defending_stats(match_id, team_id)
            }

            return {'stats': event_stats, 'status': 'success'}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def get_player_match_events(self, match_id, player_id):
        """Aggregate all events for a player in a match"""
        try:
            event_stats = {
                'shooting': self._get_player_shooting_stats(match_id, player_id),
                'passing': self._get_player_passing_stats(match_id, player_id),
                'defending': self._get_player_defending_stats(match_id, player_id)
            }

            return {'stats': event_stats, 'status': 'success'}

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def _get_possession_stats(self, match_id, team_id):
        """Calculate possession-related stats"""
        return PossessionEvent.objects.filter(
            match_id=match_id,
            team_id=team_id
        ).aggregate(
            touches=Count('touches', filter=Q(touches=True)),
            possession_lost=Count('dispossessed', filter=Q(dispossessed=True)),
            dribbles_won=Count('dribble_won', filter=Q(dribble_won=True)),
            dribbles_lost=Count('dribble_lost', filter=Q(dribble_lost=True))
        )

    def _get_shooting_stats(self, match_id, team_id):
        """Calculate shooting-related stats"""
        return ShootingEvent.objects.filter(
            match_id=match_id,
            team_id=team_id
        ).aggregate(
            total_shots=Count('is_shot', filter=Q(is_shot=True)),
            shots_on_target=Count(
                'shot_on_target', filter=Q(
                    shot_on_target=True)),
            goals=Count('is_goal', filter=Q(is_goal=True)),
            big_chances=Count(
                'id', filter=Q(
                    big_chance_scored=True) | Q(
                    big_chance_missed=True))
        )

    def _get_passing_stats(self, match_id, team_id):
        """Calculate passing-related stats"""
        return PassEvent.objects.filter(
            match_id=match_id,
            team_id=team_id
        ).aggregate(
            total_passes=Count('id'),
            accurate_passes=Count(
                'pass_accurate', filter=Q(
                    pass_accurate=True)),
            key_passes=Count('pass_key', filter=Q(pass_key=True)),
            assists=Count('assist', filter=Q(assist=True)),
            big_chances_created=Count(
                'big_chance_created', filter=Q(
                    big_chance_created=True))
        )

    def _get_defending_stats(self, match_id, team_id):
        """Calculate defending-related stats"""
        return DefendingEvent.objects.filter(
            match_id=match_id,
            team_id=team_id
        ).aggregate(
            tackles_won=Count('tackle_won', filter=Q(tackle_won=True)),
            interceptions=Count(
                'interception_won', filter=Q(
                    interception_won=True)),
            clearances=Count('is_clearance', filter=Q(is_clearance=True)),
            blocks=Count('outfielder_block', filter=Q(outfielder_block=True))
        )

    def _get_player_shooting_stats(self, match_id, player_id):
        """Calculate player shooting stats"""
        return ShootingEvent.objects.filter(
            match_id=match_id,
            player_id=player_id
        ).aggregate(
            shots=Count('is_shot', filter=Q(is_shot=True)),
            shots_on_target=Count(
                'shot_on_target', filter=Q(
                    shot_on_target=True)),
            goals=Count('is_goal', filter=Q(is_goal=True)),
            big_chances=Count(
                'id', filter=Q(
                    big_chance_scored=True) | Q(
                    big_chance_missed=True))
        )

    def _get_player_passing_stats(self, match_id, player_id):
        """Calculate player passing stats"""
        stats = PassEvent.objects.filter(
            match_id=match_id,
            player_id=player_id
        ).aggregate(
            passes_attempted=Count('id'),
            passes_completed=Count(
                'pass_accurate', filter=Q(
                    pass_accurate=True)),
            key_passes=Count('pass_key', filter=Q(pass_key=True)),
            assists=Count('assist', filter=Q(assist=True))
        )

        # Calculate pass accuracy if there were attempts
        if stats['passes_attempted'] > 0:
            stats['pass_accuracy'] = (
                stats['passes_completed'] / stats['passes_attempted']) * 100
        else:
            stats['pass_accuracy'] = 0

        return stats

    def _get_player_defending_stats(self, match_id, player_id):
        """Calculate player defending stats"""
        return DefendingEvent.objects.filter(
            match_id=match_id,
            player_id=player_id
        ).aggregate(
            tackles=Count('is_tackle', filter=Q(is_tackle=True)),
            interceptions=Count(
                'is_interception', filter=Q(
                    is_interception=True)),
            ball_recoveries=Count(
                'is_ball_recovery', filter=Q(
                    is_ball_recovery=True)),
            duels_won=Count('defensive_duel', filter=Q(defensive_duel=True))
        )
