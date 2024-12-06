from api.core.imports import *


class PlayerMatchTouchesView(BaseStatsBombView):
    touch_types = [
        'Pass', 'Ball Receipt*', 'Carry', 'Clearance',
        'Foul Won', 'Block', 'Ball Recovery', 'Duel',
        'Dribble', 'Interception', 'Miscontrol', 'Shot'
    ]

    def get(self, request, match_id, player_name):
        try:
            logger.info(
                f"Fetching touch data for player {player_name} in match {match_id}")
            match_events = sb.events(match_id=match_id)

            touches = self._get_player_touches(match_events, player_name)

            if touches.empty:
                return Response({
                    'error': f'No touch events found for player {player_name}'
                }, status=HTTP_404_NOT_FOUND)

            return Response(self._process_touches_data(touches))

        except Exception as e:
            logger.error(f"Error in PlayerMatchTouchesView: {str(e)}")
            return self.handle_error(
                e, f"Failed to fetch touch data for player {player_name}")

    def _get_player_touches(self, match_events, player_name):
        """Get all touch events for a player"""
        return match_events[
            (match_events['player'] == player_name) &
            (match_events['type'].isin(self.touch_types))
        ]

    def _process_touches_data(self, touches):
        """Process touches data for response"""
        return touches[['type', 'location']].to_dict(orient='records')
