# GET COMP INFO - shows season, stage and competition
# GET COMP MACTHES - shows everyhting u need/ want, season, score, time etc, referee, date
# GET MATCH LINEUPS - focuses on players, eg their name, number, if thye stayred, and why, if they got a card (and why and time)
# GET MATCH INFO - focuses on team stuff, its a list of match events it shows evryhting lineups shows the difference is that these
# are events that are in info type, tactical cnage see,
# eg start of matc formaiton change, sub time eg formation/tactic and when,
from api.core.imports import *


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

            # Define columns to keep - combine base event columns and
            # info-specific columns
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
            return self.handle_error(
                e, f"Failed to fetch match information for match {match_id}")
