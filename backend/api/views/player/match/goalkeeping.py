from api.core.imports import *


class GoalkeeperMatchView(BaseStatsBombView):
    goalkeeper_types = ['Goal Keeper']

    goalkeeper_columns = [
        "goalkeeper_body_part", "goalkeeper_end_location", "goalkeeper_lost_in_play",
        "goalkeeper_lost_out", "goalkeeper_outcome", "goalkeeper_position",
        "goalkeeper_punched_out", "goalkeeper_shot_saved_off_target",
        "goalkeeper_shot_saved_to_post", "goalkeeper_success_in_play",
        "goalkeeper_success_out", "goalkeeper_technique", "goalkeeper_type"
    ]

    def get(self, request, match_id, player_name):
        try:
            logger.info(
                f"Fetching goalkeeper data for player {player_name} in match {match_id}")
            match_events = sb.events(match_id=match_id)

            # Process data
            gk_data = self._process_goalkeeper_data(match_events, player_name)
            stats = self._calculate_goalkeeper_stats(gk_data)

            return Response({
                'player': player_name,
                'match_id': match_id,
                'statistics': stats,
                'goalkeeper_events': gk_data
            })

        except Exception as e:
            logger.error(f"Error in GoalkeeperMatchView: {str(e)}")
            return self.handle_error(e, f"Failed to fetch goalkeeper data for player {player_name}")

    def _process_goalkeeper_data(self, match_events, player_name):
        """Process raw goalkeeper data"""
        player_gk = match_events[
            (match_events['type'].isin(self.goalkeeper_types)) &
            (match_events['player'] == player_name)
        ]

        if player_gk.empty:
            raise ValueError(
                f'No goalkeeper events found for player {player_name}')

        columns_to_keep = [col for col in self.event_columns + self.goalkeeper_columns
                           if col in player_gk.columns]

        player_gk = player_gk[columns_to_keep]
        player_gk = player_gk.replace(
            {np.nan: None, np.inf: None, -np.inf: None})
        return self.clean_dataframe(player_gk)

    def _calculate_goalkeeper_stats(self, gk_data):
        """Calculate goalkeeper statistics"""
        stats = {
            'total_actions': len(gk_data),
            'actions_by_type': {},
            'saves': {},
            'distribution': {}
        }

        # Process each event to build statistics
        self._process_goalkeeper_events(gk_data, stats)

        # Calculate success rates
        self._calculate_success_rates(stats)

        return stats

    def _process_goalkeeper_events(self, gk_data, stats):
        """Process individual goalkeeper events and update statistics"""
        for event in gk_data:
            gk_type = event.get('goalkeeper_type')
            outcome = event.get('goalkeeper_outcome')

            # Count events by type
            if gk_type:
                stats['actions_by_type'][gk_type] = stats['actions_by_type'].get(
                    gk_type, 0) + 1

            # Update save statistics
            if gk_type in ['Shot Saved', 'Shot Saved Off T', 'Shot Saved To Post', 'Penalty Saved']:
                self._update_save_stats(stats, outcome)

            # Update distribution statistics
            if gk_type in ['Collected', 'Punch']:
                self._update_distribution_stats(stats, outcome)

    def _update_save_stats(self, stats, outcome):
        """Update save-related statistics"""
        stats['saves']['total'] = stats['saves'].get('total', 0) + 1

        if outcome in ['Success', 'In Play Safe']:
            stats['saves']['successful'] = stats['saves'].get(
                'successful', 0) + 1

        if outcome == 'Saved Twice':
            stats['saves']['double_saves'] = stats['saves'].get(
                'double_saves', 0) + 1

    def _update_distribution_stats(self, stats, outcome):
        """Update distribution-related statistics"""
        stats['distribution']['total'] = stats['distribution'].get(
            'total', 0) + 1

        if outcome in ['Success', 'In Play Safe']:
            stats['distribution']['successful'] = stats['distribution'].get(
                'successful', 0) + 1

    def _calculate_success_rates(self, stats):
        """Calculate success rates for saves and distribution"""
        if stats['saves'].get('total', 0) > 0:
            stats['saves']['success_rate'] = round(
                (stats['saves'].get('successful', 0) /
                 stats['saves']['total']) * 100, 1
            )

        if stats['distribution'].get('total', 0) > 0:
            stats['distribution']['success_rate'] = round(
                (stats['distribution'].get('successful', 0) /
                 stats['distribution']['total']) * 100, 1
            )
