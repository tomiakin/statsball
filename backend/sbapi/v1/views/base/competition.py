from rest_framework import viewsets, generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .base import BaseViewSet
from ....models import Competition, Season
from ...serializers.base.competition import (
    CompetitionListSerializer,
    CompetitionDetailSerializer,
    SeasonSerializer
)

class CompetitionViewSet(BaseViewSet):
    """API endpoint for viewing competitions"""
    queryset = Competition.objects.all()
    lookup_field = 'competition_id'
    lookup_url_kwarg = 'competition_id'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CompetitionListSerializer
        return CompetitionDetailSerializer

class CompetitionSeasonsView(generics.ListAPIView):
    """API endpoint for viewing seasons of a competition"""
    serializer_class = SeasonSerializer
    
    def get_queryset(self):
        competition_id = self.kwargs['competition_id']
        return Season.objects.filter(competition_id=competition_id)