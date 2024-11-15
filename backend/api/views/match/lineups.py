from api.core.imports import *


class MatchLineupsView(BaseStatsBombView):
    def get(self, request, match_id):
        try:
            logger.info(f"Fetching lineups for match {match_id}")

            # Fetch lineups for the specified match
            lineups = sb.lineups(match_id=match_id)

            if not lineups:
                return Response({'error': 'No lineup data found'}, status=404)

            # Process each team's lineup
            processed_lineups = {}
            for team_name, team_data in lineups.items():
                processed_players = []

                # Iterate through each player in the lineup
                for player_index in range(len(team_data)):
                    player = team_data.iloc[player_index]

                    # Capture relevant player details
                    player_info = {
                        'player_id': player['player_id'],
                        'player_name': player['player_name'],
                        'nickname': player['player_nickname'] if 'player_nickname' in player else None,
                        'jersey_number': player['jersey_number'],
                        'country': player['country'],
                        'positions': player['positions']
                    }

                    # Capture card information if available
                    if 'cards' in player and player['cards']:
                        player_info['cards'] = player['cards']

                    # Append processed player info to the list
                    processed_players.append(player_info)

                # Add processed players list to the team
                processed_lineups[team_name] = processed_players

            # Return processed lineup data
            return Response(processed_lineups)

        except Exception as e:
            logger.error(f"Error fetching lineups: {str(e)}")
            return self.handle_error(e, "Failed to fetch match lineups")
