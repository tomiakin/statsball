from typing import Dict, Any, Tuple, Optional
import logging
from datetime import datetime
from dataclasses import dataclass
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.models import Model

from ..models import (
    Competition,
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
            competition = self._get_or_create_competition(match_data)
            teams = self._create_teams(match_data)
            match = self._create_match(match_data, competition, teams)
            
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

    def _get_or_create_competition(self, data: Dict[str, Any]) -> Model:
        """Create or retrieve competition"""
        try:
            competition, created = Competition.objects.get_or_create(
                name=data['league'],
                country=data['region'],
                season=data['season']
            )
            if created:
                logger.info(f"Created new competition: {competition}")
            return competition
        except Exception as e:
            logger.error(f"Error creating competition: {str(e)}")
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
                teams[venue] = team
            return teams
        except Exception as e:
            logger.error(f"Error creating teams: {str(e)}")
            raise

    def _create_match(self, data: Dict[str, Any], competition: Model, teams: Dict[str, Model]) -> Model:
        """Create the main match record"""
        try:
            # Parse all scores
            ht_score = ScoreData.from_string(data['htScore'])
            ft_score = ScoreData.from_string(data['ftScore'])
            et_score = None
            if data.get('etScore'):
                et_score = ScoreData.from_string(data['etScore'])

            # Create match record
            return Match.objects.create(
                match_id=data['matchId'],
                competition=competition,
                start_datetime=datetime.strptime(
                    f"{data['startDate']} {data['startTime']}", 
                    "%Y-%m-%d %H:%M:%S"
                ),
                venue=data['venueName'],
                attendance=data.get('attendance'),
                referee_id=data.get('referee', {}).get('officialId'),
                referee_name=data.get('referee', {}).get('name'),
                score=data['score'],
                home_team=teams['home'],
                away_team=teams['away'],
                home_score_ht=ht_score.home,
                away_score_ht=ht_score.away,
                home_score_ft=ft_score.home,
                away_score_ft=ft_score.away,
                home_score_et=et_score.home if et_score else None,
                away_score_et=et_score.away if et_score else None
            )
        except Exception as e:
            logger.error(f"Error creating match: {str(e)}")
            raise

    def _create_team_stats(self, match: Model, data: Dict[str, Any], teams: Dict[str, Model]) -> None:
        """Create team statistics records"""
        try:
            for venue in ['home', 'away']:
                team_data = data[venue]
                MatchTeamStats.objects.create(
                    match=match,
                    team=teams[venue],
                    is_home=(venue == 'home'),
                    field=venue,
                    average_age=team_data['averageAge'],
                    manager_name=team_data['managerName'],
                    country_name=team_data['countryName'],
                    running_score=team_data['scores']['running'],
                    stats=team_data['stats']
                )
        except Exception as e:
            logger.error(f"Error creating team stats: {str(e)}")
            raise

    def _create_formations(self, match: Model, data: Dict[str, Any], teams: Dict[str, Model]) -> None:
        """Create formation records for both teams"""
        try:
            for venue in ['home', 'away']:
                team_data = data[venue]
                team_stats = match.matchteamstats_set.get(team=teams[venue])
                
                for formation_data in team_data['formations']:
                    Formation.objects.create(
                        match_team_stats=team_stats,
                        formation_id=formation_data['formationId'],
                        formation_name=formation_data['formationName'],
                        captain_player_id=formation_data['captainPlayerId'],
                        period=formation_data['period'],
                        start_minute_expanded=formation_data['startMinuteExpanded'],
                        end_minute_expanded=formation_data['endMinuteExpanded'],
                        jersey_numbers=formation_data['jerseyNumbers'],
                        player_ids=formation_data['playerIds'],
                        formation_slots=formation_data['formationSlots'],
                        formation_positions=formation_data['formationPositions']
                    )
        except Exception as e:
            logger.error(f"Error creating formations: {str(e)}")
            raise

    def _create_players(self, match: Model, data: Dict[str, Any], teams: Dict[str, Model]) -> None:
        """Create or update player records and match-player relationships"""
        try:
            for venue in ['home', 'away']:
                team_data = data[venue]
                team = teams[venue]
                
                for player_data in team_data['players']:
                    # Get or create base player record
                    player, _ = Player.objects.get_or_create(
                        player_id=player_data['playerId'],
                        defaults={
                            'name': player_data['name'],
                            'height': player_data.get('height'),
                            'weight': player_data.get('weight')
                        }
                    )
                    
                    # Create match-specific player record
                    MatchPlayer.objects.create(
                        match=match,
                        player=player,
                        team=team,
                        shirt_no=player_data['shirtNo'],
                        position=player_data['position'],
                        field=player_data['field'],
                        is_first_eleven=player_data['isFirstEleven'],
                        is_man_of_match=player_data['isManOfTheMatch'],
                        age=player_data['age'],
                        height=player_data['height'],
                        weight=player_data['weight'],
                        stats=player_data['stats']
                    )
        except Exception as e:
            logger.error(f"Error creating players: {str(e)}")
            raise