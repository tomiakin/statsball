from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Count, Q
from itertools import chain

from ..base.base import BaseViewSet

from ....models.events import (
   DefendingEvent,
   GoalkeeperEvent, 
   PassEvent,
   PossessionEvent,
   ShootingEvent,
   SummaryEvent
)

from ...serializers.base.events import (
   BaseEventSerializer,
   get_event_serializer,
   EVENT_TYPE_SERIALIZERS
)

EVENT_TYPE_MODELS = {
   'defending': DefendingEvent,
   'goalkeeper': GoalkeeperEvent,
   'passing': PassEvent, 
   'possession': PossessionEvent,
   'shooting': ShootingEvent,
   'summary': SummaryEvent,
}

class MatchEventsViewSet(BaseViewSet):
   """ViewSet for handling all match events"""
   serializer_class = BaseEventSerializer
   
   def get_queryset(self):
       match_id = self.kwargs.get('match_id')
       event_type = self.request.query_params.get('type', None)
       
       if not match_id:
           raise ValidationError("Match ID is required")
           
       # If specific event type requested
       if event_type and event_type.lower() in EVENT_TYPE_MODELS:
           model = EVENT_TYPE_MODELS[event_type.lower()]
           return model.objects.filter(
               match_id=match_id
           ).select_related(
               'team',
               'player'
           ).order_by('minute', 'second')
       
       # If no specific type, combine all event types
       all_events = []
       for model in EVENT_TYPE_MODELS.values():
           events = model.objects.filter(
               match_id=match_id
           ).select_related(
               'team',
               'player'
           )
           all_events.append(events)
           
       # Handle None values by defaulting to 0 during sorting    
       def sort_key(x):
           return (x.minute, x.second if x.second is not None else 0)
           
       combined_events = sorted(chain(*all_events), key=sort_key)
       
       return combined_events

   def get_serializer_class(self):
       event_type = self.request.query_params.get('type')
       if event_type and event_type.lower() in EVENT_TYPE_SERIALIZERS:
           return EVENT_TYPE_SERIALIZERS[event_type.lower()]
       return BaseEventSerializer

   @action(detail=False, methods=['get'])
   def stats(self, request, match_id=None):
       """Get aggregated stats for match events"""
       stats = {
           'total_events': 0,
           'by_type': {},
           'by_team': {},
           'by_period': {
               'FirstHalf': 0,
               'SecondHalf': 0
           }
       }
       
       # Aggregate stats across all event types
       for event_type, model in EVENT_TYPE_MODELS.items():
           events = model.objects.filter(match_id=match_id)
           event_count = events.count()
           stats['total_events'] += event_count
           
           # Stats by event type
           stats['by_type'][event_type] = event_count
           
           # Stats by period
           first_half = events.filter(period='FirstHalf').count()
           second_half = events.filter(period='SecondHalf').count()
           stats['by_period']['FirstHalf'] += first_half
           stats['by_period']['SecondHalf'] += second_half
           
           # Stats by team
           team_counts = events.values(
               'team__name'
           ).annotate(
               count=Count('id')
           )
           
           for team in team_counts:
               team_name = team['team__name']
               if team_name not in stats['by_team']:
                   stats['by_team'][team_name] = 0
               stats['by_team'][team_name] += team['count']
       
       return Response({
           'status': 'success',
           'data': stats,
           'message': None
       })

class EventTypeView(generics.ListAPIView):
   """View for handling specific event types for a match"""
   
   def get_queryset(self):
       match_id = self.kwargs.get('match_id')
       event_type = self.kwargs.get('event_type', '').lower()
       
       if event_type not in EVENT_TYPE_MODELS:
           raise ValidationError(f"Invalid event type: {event_type}")
           
       model = EVENT_TYPE_MODELS[event_type]
       return model.objects.filter(
           match_id=match_id
       ).select_related(
           'team',
           'player'
       ).order_by('minute', 'second')

   def get_serializer_class(self):
       event_type = self.kwargs.get('event_type', '').lower()
       return get_event_serializer(event_type)

#   # Aerial (Type) duels (won and lost are the same, just opposite)
   # looks empty (ie no/null for evryone so may need to do aerial_success + duel OR use the type (Aerial + outomce column)
   # carries xG and xA need calculating