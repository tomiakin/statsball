from api.core.imports import *


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
