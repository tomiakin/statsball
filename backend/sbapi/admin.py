from django.contrib import admin
from django.db.models import Count
from .models import (
    Competition,
    Season,
    Team,
    Player,
    Match,
    Formation,
    MatchTeamStats,
    MatchPlayer,
    PassEvent,
    ShootingEvent,
    DefendingEvent,
    GoalkeeperEvent,
    PossessionEvent,
    SummaryEvent
)

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'get_seasons', 'get_match_count')
    list_filter = ('country',)
    search_fields = ('name', 'country')
    
    def get_seasons(self, obj):
        return ", ".join([season.name for season in obj.season_set.all()])
    get_seasons.short_description = 'Seasons'
    
    def get_match_count(self, obj):
        return obj.season_set.aggregate(
            match_count=Count('match')
        )['match_count']
    get_match_count.short_description = 'Matches'

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'competition', 'is_current', 'get_match_count')
    list_filter = ('competition', 'is_current')
    search_fields = ('name', 'competition__name')

    def get_match_count(self, obj):
        return obj.match_set.count()
    get_match_count.short_description = 'Matches'

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'name', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'country')
    list_per_page = 50

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('player_id', 'name', 'get_matches_played')
    search_fields = ('name',)
    list_filter = ('matchplayer__team',)
    list_per_page = 50

    def get_matches_played(self, obj):
        return obj.matchplayer_set.count()
    get_matches_played.short_description = 'Matches Played'

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ('match_id', 'season', 'competition', 'start_datetime', 'home_team', 
                   'score', 'away_team', 'venue')
    list_filter = ('season__competition', 'season', 'start_datetime', 'venue')
    search_fields = ('home_team__name', 'away_team__name', 'venue', 
                    'season__competition__name', 'season__name')
    date_hierarchy = 'start_datetime'
    raw_id_fields = ('home_team', 'away_team', 'season')
    list_per_page = 50

@admin.register(Formation)
class FormationAdmin(admin.ModelAdmin):
    list_display = ('match_team_stats', 'formation_name', 'period', 
                   'start_minute_expanded', 'end_minute_expanded')
    list_filter = ('formation_name', 'period')
    search_fields = ('match_team_stats__team__name',)
    list_per_page = 50

@admin.register(MatchTeamStats)
class MatchTeamStatsAdmin(admin.ModelAdmin):
    list_display = ('match', 'team', 'is_home', 'manager_name', 'average_age')
    list_filter = ('is_home',)
    search_fields = ('team__name', 'manager_name')
    raw_id_fields = ('match', 'team')
    list_per_page = 50

@admin.register(MatchPlayer)
class MatchPlayerAdmin(admin.ModelAdmin):
    list_display = ('match', 'player', 'team', 'position', 'is_first_eleven', 
                   'is_man_of_match')
    list_filter = ('position', 'is_first_eleven', 'is_man_of_match')
    search_fields = ('player__name', 'team__name')
    raw_id_fields = ('match', 'player', 'team')
    list_per_page = 50

# Base Event Admin
class BaseEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'match', 'team', 'player_name', 'minute', 'type', 
                   'outcome_type')
    list_filter = ('type', 'period', 'outcome_type')
    search_fields = ('player_name', 'team__name')
    date_hierarchy = 'match__start_datetime'
    raw_id_fields = ('match', 'team', 'player')
    ordering = ('-match__start_datetime', 'minute')
    list_per_page = 50

@admin.register(PassEvent)
class PassEventAdmin(BaseEventAdmin):
    list_display = BaseEventAdmin.list_display + ('pass_accurate', 'assist', 'pass_key')
    list_filter = BaseEventAdmin.list_filter + (
        'pass_accurate', 'assist', 'pass_key', 'big_chance_created'
    )

@admin.register(ShootingEvent)
class ShootingEventAdmin(BaseEventAdmin):
    list_display = BaseEventAdmin.list_display + ('is_goal', 'shot_on_target', 
                                                'big_chance_missed')
    list_filter = BaseEventAdmin.list_filter + (
        'is_goal', 'shot_on_target', 'big_chance_missed', 'penalty_scored'
    )

@admin.register(DefendingEvent)
class DefendingEventAdmin(BaseEventAdmin):
    list_display = BaseEventAdmin.list_display + ('tackle_won', 'interception_won', 
                                                'clearance_total')
    list_filter = BaseEventAdmin.list_filter + (
        'tackle_won', 'interception_won', 'aerial_success'
    )

@admin.register(GoalkeeperEvent)
class GoalkeeperEventAdmin(BaseEventAdmin):
    list_display = BaseEventAdmin.list_display + ('keeper_save_total', 'keeper_claim_won', 
                                                'keeper_penalty_saved')
    list_filter = BaseEventAdmin.list_filter + (
        'keeper_save_total', 'keeper_claim_won', 'keeper_penalty_saved'
    )

@admin.register(PossessionEvent)
class PossessionEventAdmin(BaseEventAdmin):
    list_display = BaseEventAdmin.list_display + ('dispossessed', 'dribble_won', 
                                                'foul_committed')
    list_filter = BaseEventAdmin.list_filter + (
        'dispossessed', 'dribble_won', 'foul_committed'
    )

@admin.register(SummaryEvent)
class SummaryEventAdmin(BaseEventAdmin):
    list_display = BaseEventAdmin.list_display + ('card_type', 'sub_on', 'sub_off')
    list_filter = BaseEventAdmin.list_filter + ('card_type', 'sub_on', 'sub_off')