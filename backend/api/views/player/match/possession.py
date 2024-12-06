from api.core.imports import *


class PlayerMatchPossessionView(BaseStatsBombView):
    possession_types = [
        'Carry', 'Dispossessed', 'Dribble', 'Foul Won', 'Miscontrol', 'Offside'
    ]

    possession_columns = [
        "dribble_no_touch", "dribble_nutmeg", "dribble_outcome", "dribble_overrun",
        "carry_end_location", "foul_won_advantage", "foul_won_defensive",
        "miscontrol_aerial_won"
    ]

    def get(self, request, match_id, player_name):
        try:
            logger.info(
                f"Fetching possession data for player {player_name} in match {match_id}")
            match_events = sb.events(match_id=match_id)

            # Process data
            possession_data = self._process_possession_data(
                match_events, player_name)
            stats = self._calculate_possession_stats(possession_data)

            return Response({
                'player': player_name,
                'match_id': match_id,
                'statistics': stats,
                'possession_events': possession_data
            })

        except Exception as e:
            logger.error(f"Error in PlayerMatchPossessionView: {str(e)}")
            return self.handle_error(
                e, f"Failed to fetch possession data for player {player_name}")

    def _process_possession_data(self, match_events, player_name):
        """Process raw possession data"""
        player_possession = match_events[
            (match_events['type'].isin(self.possession_types)) &
            (match_events['player'] == player_name)
        ]

        if player_possession.empty:
            raise ValueError(
                f'No possession events found for player {player_name}')

        columns_to_keep = [col for col in self.event_columns + self.possession_columns
                           if col in player_possession.columns]

        player_possession = player_possession[columns_to_keep]
        player_possession = player_possession.replace(
            {np.nan: None, np.inf: None, -np.inf: None})
        return self.clean_dataframe(player_possession)

    def _calculate_possession_stats(self, possession_data):
        """Calculate possession statistics"""
        stats = {
            'total_possession_actions': len(possession_data),
            'actions_by_type': {}
        }

        # Count events by type
        for event_type in self.possession_types:
            count = sum(1 for event in possession_data if event.get(
                'type') == event_type)
            if count > 0:
                stats['actions_by_type'][event_type] = count

        # Calculate dribble statistics
        stats.update(self._calculate_dribble_stats(possession_data))

        # Calculate carry statistics
        stats.update(self._calculate_carry_stats(possession_data))

        # Calculate ball control statistics
        stats['ball_losses'] = {
            'dispossessed': sum(1 for event in possession_data if event.get('type') == 'Dispossessed'),
            'miscontrol': sum(1 for event in possession_data if event.get('type') == 'Miscontrol')
        }

        # Calculate fouls won
        stats['fouls_won'] = self._calculate_fouls_won_stats(possession_data)

        # Calculate offsides
        stats['offsides'] = sum(
            1 for event in possession_data if event.get('type') == 'Offside')

        return stats

    def _calculate_dribble_stats(self, possession_data):
        """Calculate dribbling-related statistics"""
        dribbles = [event for event in possession_data if event.get(
            'type') == 'Dribble']
        if not dribbles:
            return {}

        successful_dribbles = sum(1 for dribble in dribbles if dribble.get(
            'dribble_outcome') == 'Complete')
        stats = {
            'dribble_success_rate': round((successful_dribbles / len(dribbles) * 100), 1),
            'successful_dribbles': successful_dribbles,
            'total_dribbles': len(dribbles),
            'dribbling_details': {
                'nutmegs': sum(1 for dribble in dribbles if dribble.get('dribble_nutmeg') is True),
                'overrun': sum(1 for dribble in dribbles if dribble.get('dribble_overrun') is True),
                'no_touch': sum(1 for dribble in dribbles if dribble.get('dribble_no_touch') is True)
            }
        }
        return stats

    def _calculate_carry_stats(self, possession_data):
        """Calculate carry-related statistics"""
        carries = [event for event in possession_data if event.get(
            'type') == 'Carry']
        stats = {'total_carries': len(carries)}

        if carries:
            carry_distances = []
            for carry in carries:
                start_loc = carry.get('location')
                end_loc = carry.get('carry_end_location')
                if start_loc and end_loc:
                    try:
                        distance = ((end_loc[0] - start_loc[0]) **
                                    2 + (end_loc[1] - start_loc[1])**2)**0.5
                        carry_distances.append(distance)
                    except (TypeError, IndexError):
                        continue

            if carry_distances:
                stats['average_carry_distance'] = round(
                    sum(carry_distances) / len(carry_distances), 1)

        return stats

    def _calculate_fouls_won_stats(self, possession_data):
        """Calculate fouls won statistics"""
        fouls_won = [event for event in possession_data if event.get(
            'type') == 'Foul Won']
        return {
            'total': len(fouls_won),
            'defensive_half': sum(1 for foul in fouls_won if foul.get('foul_won_defensive') is True),
            'won_advantage': sum(1 for foul in fouls_won if foul.get('foul_won_advantage') is True)
        }
