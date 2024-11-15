from api.core.imports import *

class PlayerMatchDefendingView(BaseStatsBombView):
    defending_types = [
        '50/50', 'Ball Recovery', 'Block', 'Clearance', 'Dribbled Past',
        'Duel', 'Error', 'Foul Committed', 'Interception', 'Pressure', 'Shield'
    ]

    defending_columns = [
        "block_deflection", "block_offensive", "block_save_block",
        "ball_recovery_recovery_failure", "clearance_aerial_won",
        "clearance_body_part", "clearance_head", "clearance_left_foot",
        "clearance_other", "clearance_right_foot", "counterpress",
        "duel_outcome", "duel_type", "foul_committed_advantage",
        "foul_committed_card", "foul_committed_offensive",
        "foul_committed_penalty", "foul_committed_type",
        "foul_won_advantage", "foul_won_defensive", "foul_won_penalty",
        "interception_outcome"
    ]

    def get(self, request, match_id, player_name):
        try:
            logger.info(f"Fetching defensive data for player {player_name} in match {match_id}")
            match_events = sb.events(match_id=match_id)
            
            # Process data
            defense_data = self._process_defensive_data(match_events, player_name)
            stats = self._calculate_defensive_stats(defense_data)
            
            return Response({
                'player': player_name,
                'match_id': match_id,
                'statistics': stats,
                'defensive_actions': defense_data
            })

        except Exception as e:
            logger.error(f"Error in PlayerMatchDefendingView: {str(e)}")
            return self.handle_error(e, f"Failed to fetch defensive data for player {player_name}")

    def _process_defensive_data(self, match_events, player_name):
        """Process raw defensive data"""
        player_defense = match_events[
            (match_events['type'].isin(self.defending_types)) &
            (match_events['player'] == player_name)
        ]

        if player_defense.empty:
            raise ValueError(f'No defensive events found for player {player_name}')

        columns_to_keep = [col for col in self.event_columns + self.defending_columns
                          if col in player_defense.columns]
        
        player_defense = player_defense[columns_to_keep]
        player_defense = player_defense.replace({np.nan: None, np.inf: None, -np.inf: None})
        return self.clean_dataframe(player_defense)

    def _calculate_defensive_stats(self, defense_data):
        """Calculate defensive statistics"""
        stats = {
            'total_defensive_actions': len(defense_data),
            'actions_by_type': {}
        }

        # Count events by type
        for event_type in self.defending_types:
            count = sum(1 for event in defense_data if event.get('type') == event_type)
            if count > 0:
                stats['actions_by_type'][event_type] = count

        # Calculate duel success rate
        duels = [event for event in defense_data if event.get('type') == 'Duel']
        successful_duels = sum(1 for duel in duels if duel.get('duel_outcome') == 'success')
        if duels:
            stats['duel_success_rate'] = round((successful_duels / len(duels) * 100), 1)

        # Calculate pressure success rate
        pressures = [event for event in defense_data if event.get('type') == 'Pressure']
        successful_pressures = sum(1 for pressure in pressures if pressure.get('counterpress') is True)
        if pressures:
            stats['pressure_success_rate'] = round((successful_pressures / len(pressures) * 100), 1)

        # Add additional statistics
        stats.update({
            'ball_recoveries': sum(1 for event in defense_data if event.get('type') == 'Ball Recovery'),
            'interceptions': sum(1 for event in defense_data if event.get('type') == 'Interception'),
            'fouls_committed': sum(1 for event in defense_data if event.get('type') == 'Foul Committed'),
            'cards': {
                'yellow': sum(1 for event in defense_data if event.get('foul_committed_card') == 'Yellow Card'),
                'red': sum(1 for event in defense_data if event.get('foul_committed_card') == 'Red Card')
            }
        })

        return stats