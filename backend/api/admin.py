from django.contrib import admin
from .models import League, Team, TeamParticipation, Standings

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'emblem')
    search_fields = ('name', 'code')


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name', 'crest')
    search_fields = ('name', 'short_name')


@admin.register(TeamParticipation)
class TeamParticipationAdmin(admin.ModelAdmin):
    list_display = ('team', 'league', 'position', 'playedGames', 'won', 'draw', 'lost', 'points', 'goalDifference')
    list_filter = ('league',)
    search_fields = ('team__name', 'league__name')

@admin.register(Standings)
class StandingsAdmin(admin.ModelAdmin):
    list_display = ('league', 'season', 'updated_at')
    list_filter = ('league',)
    search_fields = ('league__name', 'season')