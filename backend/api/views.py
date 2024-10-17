from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Player
from .serializers import PlayerSerializer


@api_view(['GET'])
def get_players(request):
    players = Player.objects.all()
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)
