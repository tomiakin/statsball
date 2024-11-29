from django.db import transaction
import pandas as pd
import logging  # Add this

from ..models.events import (
    PassEvent, ShootingEvent, DefendingEvent,
    GoalkeeperEvent, PossessionEvent, SummaryEvent
)
from ..models import Player  # We only need Player for direct queries

logger = logging.getLogger(__name__)


def load_match_events(match, events_df):
    """Loads all events for a match"""
    with transaction.atomic():
        for _, event in events_df.iterrows():
            try:
                # Skip 'Start' events
                event_type = str(event.get('type', '')).strip()
                if event_type == 'Start':
                    logger.info("Skipping 'Start' event")
                    continue

                # Get player if exists - safer conversion
                player = None
                if not pd.isna(event.get('playerId')):
                    try:
                        player = Player.objects.get(
                            player_id=int(float(event['playerId'])))
                    except (ValueError, Player.DoesNotExist):
                        logger.warning(
                            f"Player not found or invalid ID: {event['playerId']}")

                # Get team - with safety check
                team = match.home_team if str(
                    event.get('h_a', '')).lower() == 'h' else match.away_team

                # Base event data with safer gets
                base_event_data = {
                    'event_id': int(float(event.get('eventId', 0))),
                    'match': match,
                    'team': team,
                    'player': player,
                    'player_name': event.get('playerName') if not pd.isna(event.get('playerName')) else None,
                    'minute': event.get('minute'),
                    'second': event.get('second'),
                    'expanded_minute': event.get('expandedMinute'),
                    'period': event.get('period'),
                    'max_minute': event.get('maxMinute'),
                    'x': event.get('x'),
                    'y': event.get('y'),
                    'end_x': event.get('endX') if not pd.isna(event.get('endX')) else None,
                    'end_y': event.get('endY') if not pd.isna(event.get('endY')) else None,
                    'defensive_third': bool(event.get('defensiveThird', False)),
                    'mid_third': bool(event.get('midThird', False)),
                    'final_third': bool(event.get('finalThird', False)),
                    'type': str(event.get('type', '')),
                    'outcome_type': event.get('outcomeType') if not pd.isna(event.get('outcomeType')) else None,
                    'related_event_id': event.get('relatedEventId') if not pd.isna(event.get('relatedEventId')) else None,
                    'related_player_id': event.get('relatedPlayerId') if not pd.isna(event.get('relatedPlayerId')) else None,
                    'h_a': str(event.get('h_a', '')),
                    'situation': event.get('situation') if not pd.isna(event.get('situation')) else None,
                    'qualifiers': event.get('qualifiers').tolist() if hasattr(event.get('qualifiers'), 'tolist') else event.get('qualifiers', []),
                    'satisfied_events_types': event.get('satisfiedEventsTypes').tolist() if hasattr(event.get('satisfiedEventsTypes'), 'tolist') else event.get('satisfiedEventsTypes', [])
                }

                # Route to appropriate event handler
                try:
                    if event_type == 'Pass':
                        _update_or_create_pass_event(event, base_event_data)
                    elif event_type in ['Tackle', 'Interception', 'Clearance', 'BallRecovery', 'Aerial', 'Challenge']:
                        _update_or_create_defending_event(
                            event, base_event_data)
                    elif event_type in ['Save', 'SavedShot'] or any(event.get(f'keeper_{x}', False) for x in ['save', 'claim', 'punch']):
                        _update_or_create_goalkeeper_event(
                            event, base_event_data)
                    elif event_type == 'Shot' or event.get('isShot', False):
                        _update_or_create_shooting_event(
                            event, base_event_data)
                    elif event_type in ['BallTouch', 'TakeOn', 'Dispossessed', 'Foul']:
                        _update_or_create_possession_event(
                            event, base_event_data)
                    elif event_type in ['Card', 'SubstitutionOn', 'SubstitutionOff']:
                        _update_or_create_summary_event(event, base_event_data)
                    else:
                        logger.warning(f"Unknown event type: {event_type}")
                except Exception as e:
                    logger.error(
                        f"Error processing event type {event_type}: {str(e)}")
                    continue

            except Exception as e:
                logger.error(
                    f"Error processing event {event.get('eventId')}: {str(e)}")
                continue


def _update_or_create_pass_event(event, base_data):
    """Updates or creates a passing event"""
    try:
        pass_data = {
            # Core pass attributes
            'pass_accurate': event.get('passAccurate', False),
            'pass_inaccurate': event.get('passInaccurate', False),
            'pass_accuracy': event.get('passAccuracy', False),

            # Assist types
            'assist': event.get('assist', False),
            'assist_corner': event.get('assistCorner', False),
            'assist_cross': event.get('assistCross', False),
            'assist_freekick': event.get('assistFreekick', False),
            'assist_other': event.get('assistOther', False),
            'assist_throughball': event.get('assistThroughball', False),
            'assist_throwin': event.get('assistThrowin', False),
            'intentional_assist': event.get('intentionalAssist', False),

            # Key pass types
            'key_pass_corner': event.get('keyPassCorner', False),
            'key_pass_cross': event.get('keyPassCross', False),
            'key_pass_freekick': event.get('keyPassFreekick', False),
            'key_pass_long': event.get('keyPassLong', False),
            'key_pass_other': event.get('keyPassOther', False),
            'key_pass_short': event.get('keyPassShort', False),
            'key_pass_throughball': event.get('keyPassThroughball', False),
            'key_pass_throwin': event.get('keyPassThrowin', False),
            'pass_key': event.get('passKey', False),

            # Corner passes
            'pass_corner': event.get('passCorner', False),
            'pass_corner_accurate': event.get('passCornerAccurate', False),
            'pass_corner_inaccurate': event.get('passCornerInaccurate', False),

            # Cross passes
            'pass_cross_accurate': event.get('passCrossAccurate', False),
            'pass_cross_blocked_defensive': event.get('passCrossBlockedDefensive', False),
            'pass_cross_inaccurate': event.get('passCrossInaccurate', False),

            # Freekick passes
            'pass_freekick': event.get('passFreekick', False),
            'pass_freekick_accurate': event.get('passFreekickAccurate', False),
            'pass_freekick_inaccurate': event.get('passFreekickInaccurate', False),

            # Direction/zone
            'pass_back': event.get('passBack', False),
            'pass_back_zone_inaccurate': event.get('passBackZoneInaccurate', False),
            'pass_forward': event.get('passForward', False),
            'pass_forward_zone_accurate': event.get('passForwardZoneAccurate', False),
            'pass_left': event.get('passLeft', False),
            'pass_right': event.get('passRight', False),

            # Pass types
            'pass_chipped': event.get('passChipped', False),
            'pass_head': event.get('passHead', False),
            'pass_left_foot': event.get('passLeftFoot', False),
            'pass_right_foot': event.get('passRightFoot', False),

            # Long/short passes
            'pass_long_ball_accurate': event.get('passLongBallAccurate', False),
            'pass_long_ball_inaccurate': event.get('passLongBallInaccurate', False),
            'short_pass_accurate': event.get('shortPassAccurate', False),
            'short_pass_inaccurate': event.get('shortPassInaccurate', False),

            # Through balls
            'pass_through_ball_accurate': event.get('passThroughBallAccurate', False),
            'pass_through_ball_inaccurate': event.get('passThroughBallInaccurate', False),

            # Additional characteristics
            'big_chance_created': event.get('bigChanceCreated', False),
            'successful_final_third_passes': event.get('successfulFinalThirdPasses', False),
            'throw_in': event.get('throwIn', False),
        }

        PassEvent.objects.update_or_create(
            match=base_data['match'],
            event_id=base_data['event_id'],
            defaults={**base_data, **pass_data}
        )

    except Exception as e:
        logger.error(f"Error creating/updating pass event: {str(e)}")
        raise


def _update_or_create_defending_event(event, base_data):
    """Updates or creates a defending event"""
    try:
        defending_data = {
            # Core defensive actions - determined by event type
            'is_tackle': event['type'] == 'Tackle',
            'is_interception': event['type'] == 'Interception',
            'is_clearance': event['type'] == 'Clearance',
            'is_ball_recovery': event['type'] == 'BallRecovery',

            # Aerial duels
            'aerial_success': event.get('aerialSuccess', False),
            'duel_aerial_lost': event.get('duelAerialLost', False),
            'duel_aerial_won': event.get('duelAerialWon', False),

            # Block details
            'blocked_x': event['blockedX'] if not pd.isna(event.get('blockedX')) else None,
            'blocked_y': event['blockedY'] if not pd.isna(event.get('blockedY')) else None,

            # Clearances
            'clearance_effective': event.get('clearanceEffective', False),
            'clearance_head': event.get('clearanceHead', False),
            'clearance_off_the_line': event.get('clearanceOffTheLine', False),
            'clearance_total': event.get('clearanceTotal', False),

            # Different types of duels
            'challenge_lost': event.get('challengeLost', False),
            'defensive_duel': event.get('defensiveDuel', False),
            'offensive_duel': event.get('offensiveDuel', False),

            # Defensive errors
            'error_leads_to_goal': event.get('errorLeadsToGoal', False),
            'error_leads_to_shot': event.get('errorLeadsToShot', False),
            'goal_own': event.get('goalOwn', False),

            # Interceptions
            'interception_all': event.get('interceptionAll', False),
            'interception_in_the_box': event.get('interceptionIntheBox', False),
            'interception_won': event.get('interceptionWon', False),

            # Blocks
            'outfielder_block': event.get('outfielderBlock', False),
            'outfielder_blocked_pass': event.get('outfielderBlockedPass', False),
            'six_yard_block': event.get('sixYardBlock', False),

            # Tackles
            'tackle_last_man': event.get('tackleLastMan', False),
            'tackle_lost': event.get('tackleLost', False),
            'tackle_won': event.get('tackleWon', False),

            # Other
            'penalty_conceded': event.get('penaltyConceded', False),
        }

        DefendingEvent.objects.update_or_create(
            match=base_data['match'],
            event_id=base_data['event_id'],
            defaults={**base_data, **defending_data}
        )

    except Exception as e:
        logger.error(f"Error creating/updating defending event: {str(e)}")
        raise


def _update_or_create_shooting_event(event, base_data):
    try:
        shooting_data = {
            # Big chances
            'big_chance_missed': event.get('bigChanceMissed', False),
            'big_chance_scored': event.get('bigChanceScored', False),

            # Close misses
            'close_miss_high': event.get('closeMissHigh', False),
            'close_miss_high_left': event.get('closeMissHighLeft', False),
            'close_miss_high_right': event.get('closeMissHighRight', False),
            'close_miss_left': event.get('closeMissLeft', False),
            'close_miss_right': event.get('closeMissRight', False),

            # Goals
            'is_goal': event.get('isGoal', False),
            'goal_counter': event.get('goalCounter', False),
            'goal_head': event.get('goalHead', False),
            'goal_left_foot': event.get('goalLeftFoot', False),
            'goal_right_foot': event.get('goalRightFoot', False),
            'goal_normal': event.get('goalNormal', False),
            'goal_open_play': event.get('goalOpenPlay', False),
            'goal_set_piece': event.get('goalSetPiece', False),

            # Goal location
            'goal_obox': event.get('goalObox', False),
            'goal_obp': event.get('goalObp', False),
            'goal_penalty_area': event.get('goalPenaltyArea', False),
            'goal_six_yard_box': event.get('goalSixYardBox', False),
            'goal_mouth_y': event['goalMouthY'] if not pd.isna(event.get('goalMouthY')) else None,
            'goal_mouth_z': event['goalMouthZ'] if not pd.isna(event.get('goalMouthZ')) else None,

            # Shot flags
            'is_shot': event.get('isShot', False),
            'shot_blocked': event.get('shotBlocked', False),
            'shot_counter': event.get('shotCounter', False),
            'shot_direct_corner': event.get('shotDirectCorner', False),
            'shot_on_post': event.get('shotOnPost', False),
            'shot_on_target': event.get('shotOnTarget', False),
            'shot_off_target': event.get('shotOffTarget', False),
            'shot_off_target_inside_box': event.get('shotOffTargetInsideBox', False),
            'shots_total': event.get('shotsTotal', False),

            # Shot body part
            'shot_body_type': event['shotBodyType'] if not pd.isna(event.get('shotBodyType')) else None,
            'shot_head': event.get('shotHead', False),
            'shot_left_foot': event.get('shotLeftFoot', False),
            'shot_right_foot': event.get('shotRightFoot', False),

            # Shot location
            'shot_obox_total': event.get('shotOboxTotal', False),
            'shot_obp': event.get('shotObp', False),
            'shot_penalty_area': event.get('shotPenaltyArea', False),
            'shot_six_yard_box': event.get('shotSixYardBox', False),

            # Shot type
            'shot_open_play': event.get('shotOpenPlay', False),
            'shot_set_piece': event.get('shotSetPiece', False),

            # Penalties
            'penalty_missed': event.get('penaltyMissed', False),
            'penalty_scored': event.get('penaltyScored', False),
            'penalty_shootout_missed_off_target': event.get('penaltyShootoutMissedOffTarget', False),
            'penalty_shootout_scored': event.get('penaltyShootoutScored', False),
        }

        ShootingEvent.objects.update_or_create(
            match=base_data['match'],
            event_id=base_data['event_id'],
            defaults={**base_data, **shooting_data}
        )
    except Exception as e:
        logger.error(f"Error creating/updating shooting event: {str(e)}")
        raise


def _update_or_create_goalkeeper_event(event, base_data):
    try:
        """Creates a goalkeeper event with all keeper-specific fields"""
        goalkeeper_data = {
            # Core actions
            'is_collected': event.get('collected', False),

            # Claims
            'keeper_claim_high_lost': event.get('keeperClaimHighLost', False),
            'keeper_claim_high_won': event.get('keeperClaimHighWon', False),
            'keeper_claim_lost': event.get('keeperClaimLost', False),
            'keeper_claim_won': event.get('keeperClaimWon', False),

            # Save types
            'keeper_diving_save': event.get('keeperDivingSave', False),
            'keeper_missed': event.get('keeperMissed', False),
            'keeper_one_to_one_won': event.get('keeperOneToOneWon', False),
            'standing_save': event.get('standingSave', False),
            'save_feet': event.get('saveFeet', False),
            'save_hands': event.get('saveHands', False),

            # Save locations
            'save_high_centre': event.get('saveHighCentre', False),
            'save_high_left': event.get('saveHighLeft', False),
            'save_high_right': event.get('saveHighRight', False),
            'save_low_centre': event.get('saveLowCentre', False),
            'save_low_left': event.get('saveLowLeft', False),
            'save_low_right': event.get('saveLowRight', False),

            # Save zones
            'save_obox': event.get('saveObox', False),
            'save_obp': event.get('saveObp', False),
            'save_penalty_area': event.get('savePenaltyArea', False),
            'save_six_yard_box': event.get('saveSixYardBox', False),
            'keeper_save_in_the_box': event.get('keeperSaveInTheBox', False),
            'keeper_save_total': event.get('keeperSaveTotal', False),

            # Penalties
            'keeper_penalty_saved': event.get('keeperPenaltySaved', False),
            'penalty_shootout_saved': event.get('penaltyShootoutSaved', False),
            'penalty_shootout_saved_gk': event.get('penaltyShootoutSavedGK', False),
            'penalty_shootout_conceded_gk': event.get('penaltyShootoutConcededGK', False),

            # Other actions
            'keeper_smother': event.get('keeperSmother', False),
            'keeper_sweeper_lost': event.get('keeperSweeperLost', False),
            'parried_danger': event.get('parriedDanger', False),
            'parried_safe': event.get('parriedSafe', False),
            'punches': event.get('punches', False),
        }

        GoalkeeperEvent.objects.update_or_create(
            match=base_data['match'],
            event_id=base_data['event_id'],
            defaults={**base_data, **goalkeeper_data}
        )
    except Exception as e:
        logger.error(f"Error creating/updating goalkeeper event: {str(e)}")
        raise

def _update_or_create_possession_event(event, base_data):
    
    try:
        """Creates a possession event with all possession-specific fields"""
        possession_data = {
            # Set pieces
            'corner_awarded': event.get('cornerAwarded', False),

            # Ball control
            'dispossessed': event.get('dispossessed', False),
            'touches': event.get('touches', False),
            'turnover': event.get('turnover', False),
            'overrun': event.get('overrun', False),
            'is_touch': event.get('isTouch', False),

            # Dribbling
            'dribble_lastman': event.get('dribbleLastman', False),
            'dribble_lost': event.get('dribbleLost', False),
            'dribble_won': event.get('dribbleWon', False),

            # Fouls
            'foul_committed': event.get('foulCommitted', False),
            'foul_given': event.get('foulGiven', False),
            'penalty_won': event.get('penaltyWon', False),

            # Offsides
            'offside_given': event.get('offsideGiven', False),
            'offside_provoked': event.get('offsideProvoked', False),
        }

        PossessionEvent.objects.update_or_create(
            match=base_data['match'],
            event_id=base_data['event_id'],
            defaults={**base_data, **possession_data}
        )

    except Exception as e:
        logger.error(f"Error creating/updating possession event: {str(e)}")
        raise

def _update_or_create_summary_event(event, base_data):
    try:

        """Creates a summary event with all summary-specific fields"""
        summary_data = {
            # Cards
            'card_type': event['cardType'] if not pd.isna(event.get('cardType')) and event['cardType'] != 'False' else None,
            'yellow_card': event.get('yellowCard', False),
            'red_card': event.get('redCard', False),
            'second_yellow': event.get('secondYellow', False),
            'void_yellow_card': event.get('voidYellowCard', False),

            # Substitutions
            'sub_on': event.get('subOn', False),
            'sub_off': event.get('subOff', False),
        }

        SummaryEvent.objects.update_or_create(
            match=base_data['match'],
            event_id=base_data['event_id'],
            defaults={**base_data, **summary_data}
        )
    except Exception as e:
        logger.error(f"Error creating/updating summary event: {str(e)}")
        raise
