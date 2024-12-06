from django.db.models import Count, Avg, Sum, F, Q, Case, When, FloatField
from django.db.models.functions import Cast
from sbapi.models import Team, Match
from ..events.event_aggregator import EventAggregator

class TeamStatsService:
    def __init__(self):
        self.event_aggregator = EventAggregator()

    def calculate_match_stats(self, match_id, team_id):
        """Calculate detailed team stats for a match"""
        try:
            # Get base match info
            match = Match.objects.select_related(
                'home_team',
                'away_team'
            ).get(match_id=match_id)
            
            # Verify team participated in match
            if team_id not in [match.home_team_id, match.away_team_id]:
                return {
                    'status': 'error',
                    'message': f'Team {team_id} did not participate in match {match_id}'
                }
            
            # Add team context for serializer
            match.team = match.home_team if match.home_team_id == team_id else match.away_team
            
            # Get event-based stats
            event_stats = self.event_aggregator.get_team_match_events(match_id, team_id)
            
            if event_stats['status'] == 'error':
                return event_stats
            
            # Calculate possession percentage if not already included
            if 'possession' not in event_stats['stats']:
                total_touches = event_stats['stats']['possession'].get('touches', 0)
                opponent_id = match.away_team_id if team_id == match.home_team_id else match.home_team_id
                opponent_stats = self.event_aggregator.get_team_match_events(match_id, opponent_id)
                if opponent_stats['status'] == 'success':
                    opponent_touches = opponent_stats['stats']['possession'].get('touches', 0)
                    if total_touches + opponent_touches > 0:
                        possession_pct = (total_touches / (total_touches + opponent_touches)) * 100
                        event_stats['stats']['possession']['possession_pct'] = round(possession_pct, 1)
                    else:
                        event_stats['stats']['possession']['possession_pct'] = 0
                        
            # Calculate pass accuracy if not already included
            if 'pass_accuracy' not in event_stats['stats'].get('passing', {}):
                total_passes = event_stats['stats']['passing'].get('total_passes', 0)
                accurate_passes = event_stats['stats']['passing'].get('accurate_passes', 0)
                if total_passes > 0:
                    pass_accuracy = (accurate_passes / total_passes) * 100
                    event_stats['stats']['passing']['pass_accuracy'] = round(pass_accuracy, 1)
                else:
                    event_stats['stats']['passing']['pass_accuracy'] = 0
                
            return {
                'match': match,
                'event_stats': event_stats['stats'],
                'status': 'success'
            }
            
        except Match.DoesNotExist:
            return {
                'status': 'error',
                'message': f'Match {match_id} not found'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def calculate_season_stats(self, competition_id, season_id, team_id):
        """Calculate season aggregated stats for a team"""
        try:
            # Get all matches for the team in this season
            matches = (
                Match.objects
                .filter(
                    Q(home_team_id=team_id) | Q(away_team_id=team_id),
                    season__competition_id=competition_id,
                    season_id=season_id
                )
                .select_related('home_team', 'away_team', 'season')
            )

            if not matches.exists():
                return {
                    'status': 'error',
                    'message': f'No matches found for team {team_id} in season {season_id}'
                }

            # Get team info from first match
            first_match = matches.first()
            team = first_match.home_team if first_match.home_team_id == team_id else first_match.away_team
            match_count = matches.count()

            # Initialize aggregated stats with properly formatted team dict
            stats = {
                'team': {
                    'team_id': team.team_id,  # Changed from id to team_id
                    'name': team.name,
                    'country': team.country
                },
                'matches_played': match_count,
                'home_matches': matches.filter(home_team_id=team_id).count(),
                'away_matches': matches.filter(away_team_id=team_id).count(),
                'avg_possession': 0,
                'total_shots': 0,
                'shots_on_target': 0,
                'goals_for': 0,
                'total_passes': 0,
                'accurate_passes': 0,
                'key_passes': 0,
                'assists': 0,
                'tackles_won': 0,
                'interceptions': 0,
                'clearances': 0
            }

        # Rest of the method remains the same...

            # Calculate goals
            goals = matches.aggregate(
                goals_for=Sum(Case(
                    When(home_team_id=team_id, then='home_score_ft'),
                    When(away_team_id=team_id, then='away_score_ft'),
                    default=0,
                    output_field=FloatField()
                ))
            )
            stats['goals_for'] = goals['goals_for'] or 0

            # Calculate average age
            ages = matches.aggregate(
                avg_age=Avg(Case(
                    When(home_team_id=team_id, then='home_team_average_age'),
                    When(away_team_id=team_id, then='away_team_average_age'),
                    default=None,
                    output_field=FloatField()
                ))
            )
            stats['avg_age'] = round(ages['avg_age'], 1) if ages['avg_age'] else None

            # Get latest match info
            latest_match = matches.order_by('-start_datetime').first()
            if latest_match:
                stats['manager'] = (
                    latest_match.home_manager_name 
                    if latest_match.home_team_id == team_id 
                    else latest_match.away_manager_name
                )
                
                latest_formation = latest_match.formation_set.filter(
                    team_id=team_id
                ).order_by('-start_minute').first()
                
                stats['formation'] = latest_formation.formation_name if latest_formation else 'Unknown'

                # Aggregate event stats from all matches
                total_possession = 0
                for match in matches:
                    event_stats = self.event_aggregator.get_team_match_events(
                        match.match_id, 
                        team_id
                    )
                    if event_stats['status'] == 'success':
                        # Add up possession %
                        possession = event_stats['stats']['possession'].get('possession_pct', 0)
                        total_possession += possession
                        
                        # Add up other stats
                        shooting = event_stats['stats']['shooting']
                        stats['total_shots'] += shooting.get('total_shots', 0)
                        stats['shots_on_target'] += shooting.get('shots_on_target', 0)
                        
                        passing = event_stats['stats']['passing']
                        stats['total_passes'] += passing.get('total_passes', 0)
                        stats['accurate_passes'] += passing.get('accurate_passes', 0)
                        stats['key_passes'] += passing.get('key_passes', 0)
                        stats['assists'] += passing.get('assists', 0)
                        
                        defending = event_stats['stats']['defending']
                        stats['tackles_won'] += defending.get('tackles_won', 0)
                        stats['interceptions'] += defending.get('interceptions', 0)
                        stats['clearances'] += defending.get('clearances', 0)

                # Calculate averages
                if match_count > 0:
                    stats['avg_possession'] = round(total_possession / match_count, 1)
                    stats['avg_shots'] = round(stats['total_shots'] / match_count, 1)
                    stats['avg_passes'] = round(stats['total_passes'] / match_count, 1)

                # Calculate pass accuracy
                if stats['total_passes'] > 0:
                    stats['pass_accuracy'] = round(
                        (stats['accurate_passes'] / stats['total_passes']) * 100, 
                        1
                    )
                else:
                    stats['pass_accuracy'] = 0

            return {
                'stats': stats,
                'status': 'success'
            }

        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }