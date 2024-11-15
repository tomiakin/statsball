from api.core.imports import *

class PlayerMatchPassingView(BaseStatsBombView):
    passing_columns = [
        'pass_aerial_won', 'pass_angle', 'pass_assisted_shot_id', 'pass_backheel',
        'pass_body_part', 'pass_cross', 'pass_cut_back', 'pass_deflected',
        'pass_end_location', 'pass_goal_assist', 'pass_height', 'pass_inswinging',
        'pass_length', 'pass_miscommunication', 'pass_no_touch', 'pass_outcome',
        'pass_outswinging', 'pass_recipient', 'pass_recipient_id', 'pass_shot_assist',
        'pass_straight', 'pass_switch', 'pass_technique', 'pass_through_ball', 'pass_type'
    ]

    def get(self, request, match_id, player_name):
        try:
            logger.info(f"Fetching passing data for player {player_name} in match {match_id}")
            match_events = sb.events(match_id=match_id)

            # Filter for passing events
            player_passes = match_events[
                (match_events['type'] == 'Pass') &
                (match_events['player'] == player_name)
            ]

            if player_passes.empty:
                return Response({
                    'error': f'No passing events found for player {player_name}'
                }, status=HTTP_404_NOT_FOUND)

            # Process data
            passes_data = self._process_passing_data(player_passes)
            stats = self._calculate_passing_stats(passes_data)

            return Response({
                'player': player_name,
                'match_id': match_id,
                'statistics': stats,
                'passes': passes_data
            })

        except Exception as e:
            logger.error(f"Error in PlayerMatchPassingView: {str(e)}")
            return self.handle_error(e, f"Failed to fetch passing data for player {player_name}")

    def _process_passing_data(self, player_passes):
        """Process raw passing data"""
        # Keep only relevant columns
        columns_to_keep = [col for col in self.event_columns + self.passing_columns
                          if col in player_passes.columns]
        player_passes = player_passes[columns_to_keep]
        
        # Replace NaN, inf, and -inf values before cleaning
        player_passes = player_passes.replace({
            np.nan: None,
            np.inf: None,
            -np.inf: None
        })
        
        return self.clean_dataframe(player_passes)

    def _calculate_passing_stats(self, passes_data):
        """Calculate passing statistics"""
        total_passes = len(passes_data)
        # Explicitly check for None pass_outcome (completed passes)
        completed_passes = sum(1 for p in passes_data if p.get('pass_outcome') is None)
        
        try:
            pass_completion_rate = (completed_passes / total_passes * 100) if total_passes > 0 else 0
        except (ZeroDivisionError, TypeError):
            pass_completion_rate = 0
            
        # Explicitly check for True values
        assists = sum(1 for p in passes_data if p.get('pass_goal_assist') is True)
        key_passes = sum(1 for p in passes_data if p.get('pass_shot_assist') is True)
            
        return {
            'total_passes': total_passes,
            'completed_passes': completed_passes,
            'completion_rate': round(float(pass_completion_rate), 1),
            'assists': assists,
            'key_passes': key_passes
        }