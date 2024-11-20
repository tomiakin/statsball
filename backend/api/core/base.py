from rest_framework.views import APIView
from rest_framework.response import Response
import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

class BaseStatsBombView(APIView):
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

        # First, handle all numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            df[col] = df[col].replace({
                np.nan: None,
                np.inf: None,
                -np.inf: None
            })

        # Handle all object/string columns
        object_cols = df.select_dtypes(include=['object']).columns
        for col in object_cols:
            df[col] = df[col].replace({np.nan: None})

        # Convert DataFrame to records
        records = df.to_dict(orient='records')

        # Final cleanup to ensure JSON serialization will work
        clean_records = []
        for record in records:
            clean_record = {}
            for key, value in record.items():
                if isinstance(value, np.integer):
                    clean_record[key] = int(value)
                elif isinstance(value, np.floating):
                    clean_record[key] = float(value) if not np.isnan(value) else None
                elif isinstance(value, (np.ndarray, list)):
                    # Handle array-like values
                    if isinstance(value, np.ndarray):
                        value = value.tolist()
                    clean_record[key] = [
                        None if isinstance(x, (float, np.floating)) and np.isnan(x)
                        else x for x in value
                    ]
                else:
                    clean_record[key] = None if pd.isna(value) else value
            clean_records.append(clean_record)

        return clean_records