# Returns a list of matches for a competition and season

from api.core.imports import *


class CompetitionMatchesView(BaseStatsBombView):
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
