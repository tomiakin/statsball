from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Player
from .serializers import PlayerSerializer
import requests
from django.http import JsonResponse
from decouple import config

# API im using restricts to 10 calls/min but how often do ievn need to make requests? how do i deal witht this, surely i shouldnt be reuesitng evrytime
# lets say i make a reusts for the table thne i filter by something will it make another request can i save a big fat json file in the mean time?
# this is a featre i want to have, see best form/run during the seaons/ best streaks and alos ofc worst
# add hsitorical data add ability to view standings on a particualr match day LIKE FILTERING BY MATCHDAY
# change get standings function to take in a league as a parameter so that yeah it filters
# i want to filter by matchday and season? so maybe allow it to take in match day which it can then inherit of a class basd view
# nah but on a real how often are reuqets made? like evrytime the webpage is refreshed or what
# API im using restricts to 10 calls/min but how often do ievn need to make requests? how do i deal witht this, surely i shouldnt be reuesitng evrytime
# like ofr example the prmier leageu tbnale chages on average 2/3 times a week so can i choose when to call the table

# make it delte standings of that league after every run do 1 run every 10 mins
# my vscide doenst indent the same as prettier help


@api_view(['GET'])
def get_players(request):
    players = Player.objects.all()
    serializer = PlayerSerializer(players, many=True)
    return Response(serializer.data)


def get_standings(request, standing_type): # initialise standing_type so it has one even for testing
    api_url = "https://api.football-data.org/v4/competitions/PL/standings"
    headers = {
        "X-Auth-Token": config('FOOTBALL_API_KEY')
    }
    
    # Fetch data from football-data API
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        standings_data = []

        # Filter relevant standings (Total, Home, Away)
        for standing in data['standings']:
            if standing['type'] == standing_type:
                standings_data = standing['table']
                break

        return JsonResponse({
            "competition": data['competition']['name'],
            "season": data['filters']['season'],
            "standings": standings_data
        })
    
    return JsonResponse({"error": "Unable to fetch data"}, status=400)

