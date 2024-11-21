from api.core.imports import *

class PlayerMatchShootingView(BaseStatsBombView):
    shot_columns = [
        "shot_aerial_won", "shot_body_part", "shot_deflected", "shot_end_location",
        "shot_first_time", "shot_follows_dribble"
        "shot_key_pass_id", "shot_one_on_one", "shot_open_goal", "shot_outcome",
        "shot_redirect", "shot_saved_off_target", "shot_saved_to_post",
        "shot_statsbomb_xg", "shot_technique", "shot_type", "block"
    ]

    def get(self, request, match_id, player_name):
        try:
            logger.info(f"Fetching shooting data for player {player_name} in match {match_id}")
            match_events = sb.events(match_id=match_id)
            
            # Process data
            shots_data = self._process_shooting_data(match_events, player_name)
            stats = self._calculate_shooting_stats(shots_data)
            
            return Response({
                'player': player_name,
                'match_id': match_id,
                'statistics': stats,
                'shots': shots_data
            })

        except Exception as e:
            logger.error(f"Error in PlayerMatchShootingView: {str(e)}")
            return self.handle_error(e, f"Failed to fetch shooting data for player {player_name}")

    def _process_shooting_data(self, match_events, player_name):
        """Process raw shooting data"""
        player_shots = match_events[
            (match_events['type'] == 'Shot') &
            (match_events['player'] == player_name)
        ]

        if player_shots.empty:
            raise ValueError(f'No shooting events found for player {player_name}')

        columns_to_keep = [col for col in self.event_columns + self.shot_columns
                          if col in player_shots.columns]
        
        player_shots = player_shots[columns_to_keep]
        player_shots = player_shots.replace({np.nan: None, np.inf: None, -np.inf: None})
        return self.clean_dataframe(player_shots)

    def _calculate_shooting_stats(self, shots_data):
        """Calculate shooting statistics"""
        total_shots = len(shots_data)
        goals = sum(1 for shot in shots_data if shot.get('shot_outcome') == 'Goal')
        on_target = sum(1 for shot in shots_data if shot.get('shot_outcome') in ['Goal', 'Saved', 'Saved To Post'])
        off_target = sum(1 for shot in shots_data if shot.get('shot_outcome') in ['Off T', 'Post', 'Saved Off T', 'Wayward'])
        shots_blocked = sum(1 for shot in shots_data if shot.get('shot_outcome') == 'Blocked')
        total_xg = sum(float(shot.get('shot_statsbomb_xg', 0) or 0) for shot in shots_data)

        try:
            shot_accuracy = (on_target / total_shots * 100) if total_shots > 0 else 0
            shot_conversion = (goals / total_shots * 100) if total_shots > 0 else 0
            goals_per_xg = goals / total_xg if total_xg > 0 else 0
        except (ZeroDivisionError, TypeError):
            shot_accuracy = 0
            shot_conversion = 0
            goals_per_xg = 0

        return {
            'total_shots': total_shots,
            'goals': goals,
            'shots_on_target': on_target,
            'shots_off_target': off_target,
            'shots_blocked': shots_blocked,
            'shot_accuracy': round(float(shot_accuracy), 1),
            'shot_conversion': round(float(shot_conversion), 1),
            'total_xg': round(float(total_xg), 2),
            'goals_per_xg': round(float(goals_per_xg), 2)
        }
    
    # , "shot_freeze_frame",