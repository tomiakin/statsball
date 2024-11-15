from rest_framework.views import APIView
from rest_framework.response import Response
import logging
import numpy as np

logger = logging.getLogger(__name__)

class BaseStatsBombView(APIView):

    # Common event columns used across different views
    event_columns = [
        'id', 'index', 'period', 'timestamp', 'minute', 'second', 'type',
        'possession', 'possession_team', 'play_pattern', 'team', 'player',
        'position', 'location', 'duration', 'under_pressure', 'off_camera',
        'out', 'related_events', '50_50'
    ]

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