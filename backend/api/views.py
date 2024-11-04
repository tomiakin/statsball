from rest_framework.views import APIView
from rest_framework.response import Response
from statsbombpy import sb
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class BaseStatsBombView(APIView):
    def handle_error(self, error, message="An error occurred"):
        logger.error(f"{message}: {str(error)}")
        return Response({
            'error': str(error),
            'message': message
        }, status=500)

    def clean_dataframe(self, df):
        """Clean DataFrame for JSON serialization"""
        # Make a copy to avoid modifying the original
        df = df.copy()

        # Handle the specific columns we know might have issues
        if 'last_updated_360' in df.columns:
            df['last_updated_360'] = df['last_updated_360'].replace({
                                                                    np.nan: None})

        if 'referee' in df.columns:
            df['referee'] = df['referee'].replace({np.nan: None})

        # Ensure all numeric columns are properly handled
        for col in df.select_dtypes(include=np.number).columns:
            df[col] = df[col].replace(
                {np.nan: None, np.inf: None, -np.inf: None})

        # Convert to dictionary and handle any remaining issues
        records = df.to_dict(orient='records')

        # Final cleanup to ensure JSON serialization will work
        clean_records = []
        for record in records:
            clean_record = {}
            for key, value in record.items():
                # Convert numpy integers to Python integers
                if isinstance(value, np.integer):
                    clean_record[key] = int(value)
                # Convert numpy floats to Python floats or None
                elif isinstance(value, np.floating):
                    clean_record[key] = float(
                        value) if not np.isnan(value) else None
                # Keep everything else as is
                else:
                    clean_record[key] = value
            clean_records.append(clean_record)

        return clean_records


class LeagueMatchesView(BaseStatsBombView):
    def get(self, request, competition_id, season_id):
        try:
            logger.info(
                f"Fetching matches for competition {competition_id} and season {season_id}")

            # Get matches
            matches = sb.matches(
                competition_id=competition_id, season_id=season_id)

            if matches is None or matches.empty:
                return Response({'error': 'No matches found'}, status=404)

            # Clean and convert to JSON-safe format
            matches_data = self.clean_dataframe(matches)

            return Response(matches_data)

        except Exception as e:
            logger.error(f"Error fetching matches: {str(e)}")
            return self.handle_error(e, "Failed to fetch matches")


class CompetitionInfoView(BaseStatsBombView):
    def get(self, request, competition_id, season_id):
        try:
            matches = sb.matches(
                competition_id=competition_id, season_id=season_id)

            if matches is None or matches.empty:
                return Response({'error': 'No matches found'}, status=404)

            # Clean the dataframe
            matches_data = self.clean_dataframe(matches)

            if matches_data:
                first_match = matches_data[0]
                return Response({
                    'competition': first_match.get('competition'),
                    'season': first_match.get('season'),
                    'competition_stage': first_match.get('competition_stage')
                })
            return Response({'error': 'No matches found'}, status=404)

        except Exception as e:
            return self.handle_error(e, "Failed to fetch competition info")


class CompetitionsView(BaseStatsBombView):
    def get(self, request):
        try:
            competitions = sb.competitions()
            return Response(competitions.to_dict(orient='records'))
        except Exception as e:
            return self.handle_error(e, "Failed to fetch competitions")


class SeasonsView(BaseStatsBombView):
    def get(self, request, competition_id):
        try:
            competitions = sb.competitions()
            seasons = competitions[competitions['competition_id']
                                   == competition_id]
            return Response(seasons.to_dict(orient='records'))
        except Exception as e:
            return self.handle_error(e, "Failed to fetch seasons")


class TouchDataView(BaseStatsBombView):
    def get(self, request, match_id, player_name):
        try:
            match_events = sb.events(match_id=match_id)

            touch_types = [
                'Pass', 'Ball Receipt*', 'Carry', 'Clearance',
                'Foul Won', 'Block', 'Ball Recovery', 'Duel',
                'Dribble', 'Interception', 'Miscontrol', 'Shot'
            ]

            touches = match_events[
                (match_events['player'] == player_name) &
                (match_events['type'].isin(touch_types))
            ]

            return Response(touches[['type', 'location']].to_dict(orient='records'))
        except Exception as e:
            return self.handle_error(e, "Failed to fetch touch data")
