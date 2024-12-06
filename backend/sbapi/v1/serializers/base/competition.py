from rest_framework import serializers
from sbapi.models import Competition, Season
from ..base.base import BaseSerializer, HalModelSerializer


class SeasonSerializer(BaseSerializer):
    class Meta:
        model = Season
        fields = ['season_id', 'name', 'is_current']


class CompetitionListSerializer(BaseSerializer):
    class Meta:
        model = Competition
        fields = ['competition_id', 'name', 'country']


class CompetitionDetailSerializer(HalModelSerializer):
    seasons = SeasonSerializer(source='season_set', many=True, read_only=True)

    class Meta:
        model = Competition
        fields = ['competition_id', 'name', 'country', 'seasons', '_links']

    def get__links(self, obj):
        return {
            'seasons': f'/sbapi/v1/competitions/{obj.competition_id}/seasons'
        }
