from typing import Dict, Any, Tuple, Optional
import logging
from datetime import datetime
from dataclasses import dataclass
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Model

from ..models import (
    Competition,
    Season,
    Team,
    Match,
    MatchTeamStats,
    Formation,
    Player,
    MatchPlayer
)

logger = logging.getLogger(__name__)

@dataclass
class ScoreData:
    """Structured container for match score data"""
    home: int
    away: int
    
    @classmethod
    def from_string(cls, score_str: str) -> 'ScoreData':
        """Parse score string in format '0:0' into ScoreData object"""
        try:
            home, away = map(int, score_str.split(':'))
            return cls(home=home, away=away)
        except (ValueError, AttributeError) as e:
            raise ValidationError(f"Invalid score format: {score_str}") from e

class MatchDataValidator:
    """Handles validation of match data"""
    
    REQUIRED_MATCH_FIELDS = {
        'matchId', 'league', 'region', 'season', 'home', 'away',
        'startDate', 'startTime', 'venueName', 'score', 'htScore', 'ftScore'
    }
    
    REQUIRED_TEAM_FIELDS = {
        'teamId', 'name', 'averageAge', 'managerName',
        'countryName', 'scores', 'stats', 'formations', 'players'
    }

    @classmethod
    def validate(cls, data: Dict[str, Any]) -> None:
        """Validate all match data"""
        cls._validate_required_fields(data, cls.REQUIRED_MATCH_FIELDS, "match")
        cls._validate_scores(data)
        cls._validate_teams(data)

    @staticmethod
    def _validate_required_fields(data: Dict[str, Any], required_fields: set, context: str) -> None:
        """Check for presence of required fields"""
        missing = required_fields - data.keys()
        if missing:
            raise ValidationError(f"Missing required {context} fields: {', '.join(sorted(missing))}")

    @classmethod
    def _validate_teams(cls, data: Dict[str, Any]) -> None:
        """Validate both teams' data"""
        for venue in ['home', 'away']:
            team_data = data.get(venue, {})
            if not isinstance(team_data, dict):
                raise ValidationError(f"Invalid {venue} team data format")
            cls._validate_required_fields(team_data, cls.REQUIRED_TEAM_FIELDS, f"{venue} team")

    @staticmethod
    def _validate_scores(data: Dict[str, Any]) -> None:
        """Validate all score fields"""
        for field in ['score', 'htScore', 'ftScore']:
            ScoreData.from_string(data[field])  # Will raise ValidationError if invalid

class MatchLoader:
    """Handles loading match data into the database"""

    def __init__(self):
        self.validator = MatchDataValidator()

    @transaction.atomic
    def load_match(self, match_data: Dict[str, Any]) -> Model:
        """
        Load match data into database with transaction handling
        
        Args:
            match_data: Dictionary containing match data
            
        Returns:
            Match: Created Match instance
            
        Raises:
            ValidationError: If data validation fails
            Exception: For other errors during loading
        """
        try:
            # Validate all input data
            self.validator.validate(match_data)
            
            # Load core match data
            competition, season = self._get_or_create_competition_and_season(match_data)
            teams = self._create_teams(match_data)
            match = self._create_match(match_data, competition, season, teams)
            
            # Load related data
            self._create_team_stats(match, match_data, teams)
            self._create_formations(match, match_data, teams)
            self._create_players(match, match_data, teams)
            
            logger.info(f"Successfully loaded match {match_data['matchId']}")
            return match
            
        except ValidationError as e:
            logger.error(f"Validation error for match {match_data.get('matchId')}: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Error loading match {match_data.get('matchId')}: {str(e)}")
            raise

    def _get_or_create_competition_and_season(self, data: Dict[str, Any]) -> Tuple[Model, Model]:
        """Create or retrieve competition and season"""
        try:
            # First get or create the competition
            competition, _ = Competition.objects.get_or_create(
                name=data['league'],
                country=data['region']
            )

            # Parse the season name from the data
            season_name = data['season']  # e.g., "2023/24"
            
            # Calculate approximate start and end dates based on season name
            # start_year = int(season_name.split('/')[0])
            # end_year = start_year + 1
            # start_date = datetime(start_year, 7, 1).date()  # Typical season start
            # end_date = datetime(end_year, 6, 30).date()    # Typical season end

            # Get or create the season
            season, created = Season.objects.get_or_create(
                competition=competition,
                name=season_name,
                defaults={
                    'is_current': False  # This should be managed separately
                }
            )

            if created:
                logger.info(f"Created new season: {season}")

            return competition, season
        except Exception as e:
            logger.error(f"Error creating competition and season: {str(e)}")
            raise

    def _create_teams(self, data: Dict[str, Any]) -> Dict[str, Model]:
        """Create or retrieve both teams"""
        teams = {}
        try:
            for venue in ['home', 'away']:
                team_data = data[venue]
                team, created = Team.objects.get_or_create(
                    team_id=team_data['teamId'],
                    defaults={
                        'name': team_data['name'],
                        'country': data['region']
                    }
                )
                if created:
                    logger.info(f"Created new team: {team}")
                else:
                    logger.info(f"Updated team: {team}")
                teams[venue] = team
            return teams
        except Exception as e:
            logger.error(f"Error creating or updating teams: {str(e)}")
            raise

    def _create_match(self, data: Dict[str, Any], competition: Model, season: Model, teams: Dict[str, Model]) -> Model:
        """Create or update the main match record"""
        try:
            # Parse all scores
            ht_score = ScoreData.from_string(data['htScore'])
            ft_score = ScoreData.from_string(data['ftScore'])
            et_score = None
            if data.get('etScore'):
                et_score = ScoreData.from_string(data['etScore'])

            # Parse the datetime
            start_datetime = None
            try:
                if 'T' in data['startDate']:
                    # New format: "2023-11-06T00:00:00"
                    start_date = datetime.strptime(data['startDate'].split('T')[0], "%Y-%m-%d")
                    # New format: "2023-11-06T20:00:00"
                    start_time = datetime.strptime(data['startTime'].split('T')[1], "%H:%M:%S")
                    start_datetime = datetime.combine(start_date.date(), start_time.time())
                else:
                    # Old format handling
                    start_datetime = datetime.strptime(
                        f"{data['startDate']} {data['startTime']}",
                        "%Y-%m-%d %H:%M:%S"
                    )
            except (ValueError, TypeError) as e:
                logger.error(f"Error parsing datetime: {e}")
                raise ValidationError(f"Invalid datetime format: {data['startDate']} {data['startTime']}")

            defaults = {
                'season': season,  # Add season reference
                'start_datetime': start_datetime,
                'venue': data['venueName'],
                'attendance': data.get('attendance'),
                'referee_id': data.get('referee', {}).get('officialId'),
                'referee_name': data.get('referee', {}).get('name'),
                'score': data['score'],
                'home_team': teams['home'],
                'away_team': teams['away'],
                'home_score_ht': ht_score.home,
                'away_score_ht': ht_score.away,
                'home_score_ft': ft_score.home,
                'away_score_ft': ft_score.away,
                'home_score_et': et_score.home if et_score else None,
                'away_score_et': et_score.away if et_score else None
            }

            match, created = Match.objects.update_or_create(
                match_id=data['matchId'],
                defaults=defaults
            )

            action = "Created new" if created else "Updated existing"
            logger.info(f"{action} match: {match}")
            
            return match

        except Exception as e:
            logger.error(f"Error creating or updating match {data.get('matchId')}: {str(e)}")
            raise

    def _create_team_stats(self, match: Model, data: Dict[str, Any], teams: Dict[str, Model]) -> None:
        """Create or update team statistics records"""
        try:
            for venue in ['home', 'away']:
                team_data = data[venue]
                MatchTeamStats.objects.update_or_create(
                    match=match,
                    team=teams[venue],
                    defaults={
                        'is_home': (venue == 'home'),
                        'field': venue,
                        'average_age': team_data['averageAge'],
                        'manager_name': team_data['managerName'],
                        'country_name': team_data['countryName'],
                        'running_score': team_data['scores']['running'],
                        'stats': team_data['stats']
                    }
                )
        except Exception as e:
            logger.error(f"Error creating/updating team stats: {str(e)}")
            raise

    def _create_formations(self, match: Model, data: Dict[str, Any], teams: Dict[str, Model]) -> None:
        """Create or update formation records for both teams"""
        try:
            for venue in ['home', 'away']:
                team_data = data[venue]
                team_stats = match.matchteamstats_set.get(team=teams[venue])
                
                for formation_data in team_data['formations']:
                    Formation.objects.update_or_create(
                        match_team_stats=team_stats,
                        formation_id=formation_data['formationId'],
                        period=formation_data['period'],
                        defaults={
                            'formation_name': formation_data['formationName'],
                            'captain_player_id': formation_data['captainPlayerId'],
                            'start_minute_expanded': formation_data['startMinuteExpanded'],
                            'end_minute_expanded': formation_data['endMinuteExpanded'],
                            'jersey_numbers': formation_data['jerseyNumbers'],
                            'player_ids': formation_data['playerIds'],
                            'formation_slots': formation_data['formationSlots'],
                            'formation_positions': formation_data['formationPositions']
                        }
                    )
        except Exception as e:
            logger.error(f"Error creating/updating formations: {str(e)}")
            raise

    def _create_players(self, match: Model, data: Dict[str, Any], teams: Dict[str, Model]) -> None:
        """Create or update player records and match-player relationships"""
        try:
            for venue in ['home', 'away']:
                team_data = data[venue]
                team = teams[venue]
                
                for player_data in team_data['players']:
                    # First update or create the base player record
                    try:
                        player, player_created = Player.objects.update_or_create(
                            player_id=player_data['playerId'],
                            defaults={
                                'name': player_data['name'],
                                'height': player_data.get('height'),
                                'weight': player_data.get('weight'),
                            }
                        )
                        
                        # Then update or create the match-specific player record
                        MatchPlayer.objects.update_or_create(
                            match=match,
                            player=player,
                            team=team,
                            defaults={
                                'shirt_no': player_data['shirtNo'],
                                'position': player_data['position'],
                                'field': player_data['field'],
                                'is_first_eleven': player_data.get('isFirstEleven', False),
                                'is_man_of_match': player_data.get('isManOfTheMatch', False),
                                'age': player_data.get('age', 0),
                                'height': player_data.get('height', 0),
                                'weight': player_data.get('weight', 0),
                                'stats': player_data.get('stats', {})
                            }
                        )
                        
                    except Exception as e:
                        logger.error(f"Error processing player {player_data.get('playerId')}: {str(e)}")
                        raise

        except Exception as e:
            logger.error(f"Error creating/updating players: {str(e)}")
            raise