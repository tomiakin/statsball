from rest_framework.views import APIView
from rest_framework.response import Response
from statsbombpy import sb
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


class BaseStatsBombView(APIView):

    # Common event columns used across different views
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

        # Handle the specific columns we know might have issues
        if 'last_updated_360' in df.columns:
            df['last_updated_360'] = df['last_updated_360'].replace({
                                                                    np.nan: None})

        if 'referee' in df.columns:
            df['referee'] = df['referee'].replace({np.nan: None})

        # Ensure all numeric columns are properly handled
        for col in df.select_dtypes(include=np.number).columns:
            df[col] = df[col].replace(
                {np.nan: None, np.inf: None, -np.inf: None})

        # Convert to dictionary and handle any remaining issues
        records = df.to_dict(orient='records')

        # Final cleanup to ensure JSON serialization will work
        clean_records = []
        for record in records:
            clean_record = {}
            for key, value in record.items():
                # Convert numpy integers to Python integers
                if isinstance(value, np.integer):
                    clean_record[key] = int(value)
                # Convert numpy floats to Python floats or None
                elif isinstance(value, np.floating):
                    clean_record[key] = float(
                        value) if not np.isnan(value) else None
                # Keep everything else as is
                else:
                    clean_record[key] = value
            clean_records.append(clean_record)

        return clean_records


class LeagueMatchesView(BaseStatsBombView):
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


class TouchDataView(BaseStatsBombView):
    def get(self, request, match_id, player_name):
        try:
            match_events = sb.events(match_id=match_id)

            touch_types = [
                'Pass', 'Ball Receipt*', 'Carry', 'Clearance',
                'Foul Won', 'Block', 'Ball Recovery', 'Duel',
                'Dribble', 'Interception', 'Miscontrol', 'Shot'
            ]

            touches = match_events[
                (match_events['player'] == player_name) &
                (match_events['type'].isin(touch_types))
            ]

            return Response(touches[['type', 'location']].to_dict(orient='records'))
        except Exception as e:
            return self.handle_error(e, "Failed to fetch touch data")


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
            logger.info(
                f"Fetching passing data for player {player_name} in match {match_id}")
            match_events = sb.events(match_id=match_id)

            # Filter for the specific player's passing events
            player_passes = match_events[
                (match_events['type'] == 'Pass') &
                (match_events['player'] == player_name)
            ]

            if player_passes.empty:
                return Response({
                    'error': f'No passing events found for player {player_name}'
                }, status=404)

            # Keep only columns that exist in the DataFrame
            columns_to_keep = [col for col in self.event_columns + self.passing_columns
                               if col in player_passes.columns]

            player_passes = player_passes[columns_to_keep]

            # Replace NaN values with None before cleaning
            player_passes = player_passes.replace(
                {np.nan: None, np.inf: None, -np.inf: None})
            passes_data = self.clean_dataframe(player_passes)

            # Calculate statistics safely
            total_passes = len(passes_data)
            completed_passes = sum(1 for p in passes_data
                                   if p.get('pass_outcome') is None)

            try:
                pass_completion_rate = (
                    completed_passes / total_passes * 100) if total_passes > 0 else 0
            except (ZeroDivisionError, TypeError):
                pass_completion_rate = 0

            assists = sum(1 for p in passes_data
                          if p.get('pass_goal_assist') is True)  # explicitly check for True
            key_passes = sum(1 for p in passes_data
                             if p.get('pass_shot_assist') is True)  # explicitly check for True

            return Response({
                'player': player_name,
                'match_id': match_id,
                'statistics': {
                    'total_passes': total_passes,
                    'completed_passes': completed_passes,
                    'completion_rate': round(float(pass_completion_rate), 1),
                    'assists': assists,
                    'key_passes': key_passes
                },
                'passes': passes_data
            })

        except Exception as e:
            logger.error(f"Error in PlayerMatchPassingView: {str(e)}")
            return self.handle_error(e, f"Failed to fetch passing data for player {player_name}")


class PlayerMatchShootingView(BaseStatsBombView):
    shot_columns = [
        "shot_aerial_won", "shot_body_part", "shot_deflected", "shot_end_location",
        "shot_first_time", "shot_follows_dribble", "shot_freeze_frame",
        "shot_key_pass_id", "shot_one_on_one", "shot_open_goal", "shot_outcome",
        "shot_redirect", "shot_saved_off_target", "shot_saved_to_post",
        "shot_statsbomb_xg", "shot_technique", "shot_type"
    ]

    def get(self, request, match_id, player_name):
        try:
            logger.info(
                f"Fetching shooting data for player {player_name} in match {match_id}")
            match_events = sb.events(match_id=match_id)

            player_shots = match_events[
                (match_events['type'] == 'Shot') &
                (match_events['player'] == player_name)
            ]

            if player_shots.empty:
                return Response({
                    'error': f'No shooting events found for player {player_name}'
                }, status=404)

            columns_to_keep = [col for col in self.event_columns + self.shot_columns
                               if col in player_shots.columns]

            player_shots = player_shots[columns_to_keep]

            # Replace NaN values with None before cleaning
            player_shots = player_shots.replace(
                {np.nan: None, np.inf: None, -np.inf: None})
            shots_data = self.clean_dataframe(player_shots)

            # Calculate statistics safely
            total_shots = len(shots_data)
            goals = sum(1 for shot in shots_data
                        if shot.get('shot_outcome') == 'Goal')
            on_target = sum(1 for shot in shots_data
                            if shot.get('shot_outcome') in ['Goal', 'Saved'])

            # Safely calculate xG
            total_xg = sum(float(shot.get('shot_statsbomb_xg', 0) or 0)
                           for shot in shots_data)

            try:
                shot_accuracy = (on_target / total_shots *
                                 100) if total_shots > 0 else 0
                goals_per_xg = goals / total_xg if total_xg > 0 else 0
            except (ZeroDivisionError, TypeError):
                shot_accuracy = 0
                goals_per_xg = 0

            return Response({
                'player': player_name,
                'match_id': match_id,
                'statistics': {
                    'total_shots': total_shots,
                    'goals': goals,
                    'shots_on_target': on_target,
                    'shot_accuracy': round(float(shot_accuracy), 1),
                    'total_xg': round(float(total_xg), 2),
                    'goals_per_xg': round(float(goals_per_xg), 2)
                },
                'shots': shots_data
            })

        except Exception as e:
            logger.error(f"Error in PlayerMatchShootingView: {str(e)}")
            return self.handle_error(e, f"Failed to fetch shooting data for player {player_name}")


class PlayerMatchDefendingView(BaseStatsBombView):
    # Define defensive event types and columns as class variables
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
            logger.info(
                f"Fetching defensive data for player {player_name} in match {match_id}")
            match_events = sb.events(match_id=match_id)

            # Filter for the specific player's defensive events
            player_defense = match_events[
                (match_events['type'].isin(self.defending_types)) &
                (match_events['player'] == player_name)
            ]

            if player_defense.empty:
                return Response({
                    'error': f'No defensive events found for player {player_name}'
                }, status=404)

            # Keep only columns that exist in the DataFrame
            columns_to_keep = [col for col in self.event_columns + self.defending_columns
                               if col in player_defense.columns]

            player_defense = player_defense[columns_to_keep]

            # Replace NaN values with None before cleaning
            player_defense = player_defense.replace(
                {np.nan: None, np.inf: None, -np.inf: None})
            defense_data = self.clean_dataframe(player_defense)

            # Calculate defensive statistics
            stats = {
                'total_defensive_actions': len(defense_data),
                'actions_by_type': {}
            }

            # Count events by type
            for event_type in self.defending_types:
                count = sum(1 for event in defense_data if event.get(
                    'type') == event_type)
                if count > 0:  # Only include non-zero counts
                    stats['actions_by_type'][event_type] = count

            # Calculate successful duels
            duels = [event for event in defense_data if event.get(
                'type') == 'Duel']
            successful_duels = sum(1 for duel in duels
                                   if duel.get('duel_outcome') == 'success')

            if duels:
                stats['duel_success_rate'] = round(
                    (successful_duels / len(duels) * 100), 1)

            # Calculate successful pressures (when pressure leads to defensive action)
            pressures = [event for event in defense_data if event.get(
                'type') == 'Pressure']
            successful_pressures = sum(1 for pressure in pressures
                                       if pressure.get('counterpress') is True)

            if pressures:
                stats['pressure_success_rate'] = round(
                    (successful_pressures / len(pressures) * 100), 1)

            # Add ball recoveries and interceptions
            stats['ball_recoveries'] = sum(1 for event in defense_data
                                           if event.get('type') == 'Ball Recovery')
            stats['interceptions'] = sum(1 for event in defense_data
                                         if event.get('type') == 'Interception')

            # Add fouls data
            fouls = sum(1 for event in defense_data
                        if event.get('type') == 'Foul Committed')
            stats['fouls_committed'] = fouls

            # Get cards
            yellow_cards = sum(1 for event in defense_data
                               if event.get('foul_committed_card') == 'Yellow Card')
            red_cards = sum(1 for event in defense_data
                            if event.get('foul_committed_card') == 'Red Card')

            stats['cards'] = {
                'yellow': yellow_cards,
                'red': red_cards
            }

            return Response({
                'player': player_name,
                'match_id': match_id,
                'statistics': stats,
                'defensive_actions': defense_data
            })

        except Exception as e:
            logger.error(f"Error in PlayerMatchDefendingView: {str(e)}")
            return self.handle_error(e, f"Failed to fetch defensive data for player {player_name}")


class PlayerMatchPossessionView(BaseStatsBombView):
    # Define possession event types and columns as class variables
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

            # Filter for the specific player's possession events
            player_possession = match_events[
                (match_events['type'].isin(self.possession_types)) &
                (match_events['player'] == player_name)
            ]

            if player_possession.empty:
                return Response({
                    'error': f'No possession events found for player {player_name}'
                }, status=404)

            # Keep only columns that exist in the DataFrame
            columns_to_keep = [col for col in self.event_columns + self.possession_columns
                               if col in player_possession.columns]

            player_possession = player_possession[columns_to_keep]

            # Replace NaN values with None before cleaning
            player_possession = player_possession.replace(
                {np.nan: None, np.inf: None, -np.inf: None})
            possession_data = self.clean_dataframe(player_possession)

            # Calculate possession statistics
            stats = {
                'total_possession_actions': len(possession_data),
                'actions_by_type': {}
            }

            # Count events by type
            for event_type in self.possession_types:
                count = sum(1 for event in possession_data if event.get(
                    'type') == event_type)
                if count > 0:  # Only include non-zero counts
                    stats['actions_by_type'][event_type] = count

            # Calculate dribble success rate
            dribbles = [event for event in possession_data if event.get(
                'type') == 'Dribble']
            successful_dribbles = sum(1 for dribble in dribbles
                                      if dribble.get('dribble_outcome') == 'Complete')

            if dribbles:
                stats['dribble_success_rate'] = round(
                    (successful_dribbles / len(dribbles) * 100), 1)
                stats['successful_dribbles'] = successful_dribbles
                stats['total_dribbles'] = len(dribbles)

            # Calculate carry statistics
            carries = [event for event in possession_data if event.get(
                'type') == 'Carry']
            stats['total_carries'] = len(carries)

            # Calculate average carry distance if location data is available
            if carries:
                carry_distances = []
                for carry in carries:
                    start_loc = carry.get('location')
                    end_loc = carry.get('carry_end_location')
                    if start_loc and end_loc:
                        # Calculate Euclidean distance
                        try:
                            distance = ((end_loc[0] - start_loc[0])**2 +
                                        (end_loc[1] - start_loc[1])**2)**0.5
                            carry_distances.append(distance)
                        except (TypeError, IndexError):
                            continue

                if carry_distances:
                    stats['average_carry_distance'] = round(
                        sum(carry_distances) / len(carry_distances), 1)

            # Calculate ball control statistics
            stats['ball_losses'] = {
                'dispossessed': sum(1 for event in possession_data
                                    if event.get('type') == 'Dispossessed'),
                'miscontrol': sum(1 for event in possession_data
                                  if event.get('type') == 'Miscontrol')
            }

            # Calculate fouls won
            fouls_won = [event for event in possession_data if event.get(
                'type') == 'Foul Won']
            stats['fouls_won'] = {
                'total': len(fouls_won),
                'defensive_half': sum(1 for foul in fouls_won
                                      if foul.get('foul_won_defensive') is True),
                'won_advantage': sum(1 for foul in fouls_won
                                     if foul.get('foul_won_advantage') is True)
            }

            # Calculate offsides
            stats['offsides'] = sum(1 for event in possession_data
                                    if event.get('type') == 'Offside')

            # Calculate advanced dribbling stats
            if dribbles:
                stats['dribbling_details'] = {
                    'nutmegs': sum(1 for dribble in dribbles
                                   if dribble.get('dribble_nutmeg') is True),
                    'overrun': sum(1 for dribble in dribbles
                                   if dribble.get('dribble_overrun') is True),
                    'no_touch': sum(1 for dribble in dribbles
                                    if dribble.get('dribble_no_touch') is True)
                }

            return Response({
                'player': player_name,
                'match_id': match_id,
                'statistics': stats,
                'possession_events': possession_data
            })

        except Exception as e:
            logger.error(f"Error in PlayerMatchPossessionView: {str(e)}")
            return self.handle_error(e, f"Failed to fetch possession data for player {player_name}")


class GoalkeeperMatchView(BaseStatsBombView):
    # Define goalkeeper event types and columns as class variables
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

            # Filter for the specific player's goalkeeper events
            player_gk = match_events[
                (match_events['type'].isin(self.goalkeeper_types)) &
                (match_events['player'] == player_name)
            ]

            if player_gk.empty:
                return Response({
                    'error': f'No goalkeeper events found for player {player_name}'
                }, status=404)

            # Keep only columns that exist in the DataFrame
            columns_to_keep = [col for col in self.event_columns + self.goalkeeper_columns
                               if col in player_gk.columns]

            player_gk = player_gk[columns_to_keep]

            # Replace NaN values with None before cleaning
            player_gk = player_gk.replace(
                {np.nan: None, np.inf: None, -np.inf: None})
            gk_data = self.clean_dataframe(player_gk)

            # Calculate goalkeeper statistics
            stats = {
                'total_actions': len(gk_data),
                'actions_by_type': {},
                'saves': {},
                'distribution': {}
            }

            # Process each event
            for event in gk_data:
                gk_type = event.get('goalkeeper_type')
                outcome = event.get('goalkeeper_outcome')

                # Count events by type
                if gk_type:
                    stats['actions_by_type'][gk_type] = stats['actions_by_type'].get(
                        gk_type, 0) + 1

                # Save statistics
                if gk_type in ['Shot Saved', 'Shot Saved Off T', 'Shot Saved To Post', 'Penalty Saved']:
                    stats['saves']['total'] = stats['saves'].get(
                        'total', 0) + 1
                    if outcome == 'Success' or outcome == 'In Play Safe':
                        stats['saves']['successful'] = stats['saves'].get(
                            'successful', 0) + 1
                    if outcome == 'Saved Twice':
                        stats['saves']['double_saves'] = stats['saves'].get(
                            'double_saves', 0) + 1

                # Distribution statistics
                if gk_type in ['Collected', 'Punch']:
                    stats['distribution']['total'] = stats['distribution'].get(
                        'total', 0) + 1
                    if outcome in ['Success', 'In Play Safe']:
                        stats['distribution']['successful'] = stats['distribution'].get(
                            'successful', 0) + 1

            # Calculate success rates
            if stats['saves'].get('total', 0) > 0:
                stats['saves']['success_rate'] = round(
                    (stats['saves'].get('successful', 0) / stats['saves']['total']) * 100, 1)

            if stats['distribution'].get('total', 0) > 0:
                stats['distribution']['success_rate'] = round(
                    (stats['distribution'].get('successful', 0) / stats['distribution']['total']) * 100, 1)

            return Response({
                'player': player_name,
                'match_id': match_id,
                'statistics': stats,
                'goalkeeper_events': gk_data
            })

        except Exception as e:
            logger.error(f"Error in GoalkeeperMatchView: {str(e)}")
            return self.handle_error(e, f"Failed to fetch goalkeeper data for player {player_name}")


class MatchInformationView(BaseStatsBombView):
    info_types = [
        'Bad Behaviour', 'Half End', 'Half Start', 'Injury Stoppage', 'Offside',
        'Own Goal Against', 'Own Goal For', 'Player Off', 'Player On',
        'Referee Ball-Drop', 'Starting XI', 'Substitution', 'Tactical Shift'
    ]

    def process_tactics_data(self, event):
        """Helper method to process formation and lineup data"""
        tactics_data = {}
        if 'tactics' in event:
            tactics = event.get('tactics', {})
            if tactics:
                tactics_data = {
                    'formation': tactics.get('formation'),
                    'lineup': tactics.get('lineup', [])
                }
        return tactics_data

    def get(self, request, match_id):
        try:
            logger.info(
                f"Fetching match information events for match {match_id}")
            match_events = sb.events(match_id=match_id)

            # Filter for information events
            info_events = match_events[
                match_events['type'].isin(self.info_types)
            ]

            if info_events.empty:
                return Response({
                    'error': f'No information events found for match {match_id}'
                }, status=404)

            # Define columns to keep - combine base event columns and info-specific columns
            info_columns = self.event_columns + [
                'bad_behaviour_card', 'tactics', 'replacement', 'outcome'
            ]

            # Keep only columns that exist in the DataFrame
            columns_to_keep = [col for col in info_columns
                               if col in info_events.columns]

            info_events = info_events[columns_to_keep]
            info_events = info_events.replace(
                {np.nan: None, np.inf: None, -np.inf: None})
            events_data = self.clean_dataframe(info_events)

            # Organize events by type and period
            organized_events = {
                'match_timeline': [],
                'statistics': {
                    'total_events': len(events_data),
                    'events_by_type': {},
                    'events_by_period': {},
                },
                'team_data': {
                    'starting_xi': {},
                    'substitutions': [],
                    'tactical_shifts': []
                }
            }

            # Process each event
            for event in events_data:
                event_type = event.get('type')
                period = event.get('period')
                minute = event.get('minute')
                second = event.get('second')
                team = event.get('team')

                # Base timeline event structure
                timeline_event = {
                    'type': event_type,
                    'period': period,
                    'time': f"{minute}:{str(second).zfill(2)}",
                    'team': team,
                    'player': event.get('player')
                }

                # Process specific event types
                if event_type == 'Starting XI':
                    tactics_data = self.process_tactics_data(event)
                    if tactics_data:
                        organized_events['team_data']['starting_xi'][team] = {
                            'formation': tactics_data.get('formation'),
                            'lineup': tactics_data.get('lineup'),
                            'period': period
                        }
                        timeline_event['tactics'] = tactics_data

                elif event_type == 'Substitution':
                    sub_data = {
                        'time': f"{minute}:{str(second).zfill(2)}",
                        'team': team,
                        'player_off': event.get('player'),
                        'player_on': event.get('replacement', {}).get('name'),
                        'reason': event.get('outcome', {}).get('name'),
                        'period': period
                    }
                    organized_events['team_data']['substitutions'].append(
                        sub_data)
                    timeline_event.update(sub_data)

                elif event_type == 'Tactical Shift':
                    tactics_data = self.process_tactics_data(event)
                    if tactics_data:
                        shift_data = {
                            'time': f"{minute}:{str(second).zfill(2)}",
                            'team': team,
                            'period': period,
                            'new_formation': tactics_data.get('formation'),
                            'new_lineup': tactics_data.get('lineup')
                        }
                        organized_events['team_data']['tactical_shifts'].append(
                            shift_data)
                        timeline_event.update(shift_data)

                elif event_type == 'Bad Behaviour':
                    timeline_event['card'] = event.get('bad_behaviour_card')

                # Add to timeline
                organized_events['match_timeline'].append(timeline_event)

                # Update statistics
                organized_events['statistics']['events_by_type'][event_type] = \
                    organized_events['statistics']['events_by_type'].get(
                        event_type, 0) + 1

                period_key = f"Period {period}"
                organized_events['statistics']['events_by_period'][period_key] = \
                    organized_events['statistics']['events_by_period'].get(
                        period_key, 0) + 1

            # Sort timeline by period and time
            organized_events['match_timeline'].sort(
                key=lambda x: (x['period'],
                               int(x['time'].split(':')[0]),
                               int(x['time'].split(':')[1]))
            )

            return Response({
                'match_id': match_id,
                'match_events': organized_events['match_timeline'],
                'statistics': organized_events['statistics'],
                'team_data': organized_events['team_data'],
                'raw_events': events_data
            })

        except Exception as e:
            logger.error(f"Error in MatchInformationView: {str(e)}")
            return self.handle_error(e, f"Failed to fetch match information for match {match_id}")
