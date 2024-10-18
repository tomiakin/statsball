import requests
from django.core.management.base import BaseCommand
from api.models import Team, TeamParticipation, League
from decouple import config

class Command(BaseCommand):
    help = 'Fetch and update league standings'

    leagues_dict = {
        'PL': 'Premier League',
        'BL1': 'Bundesliga',
        'CL': 'Champions League',
        # Add more leagues as needed
    }

    def handle(self, *args, **kwargs):
        for code, name in self.leagues_dict.items():
            url = f'https://api.football-data.org/v4/competitions/{code}/standings'
            headers = {
                "X-Auth-Token": config('FOOTBALL_API_KEY')
            }
            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()

                # Create or get the league
                league, created = League.objects.get_or_create(
                    code=code,
                    defaults={'name': name, 'emblem': data['competition']['emblem']}
                )

                for team_data in data['standings'][0]['table']:
                    # Create or get the team
                    team, created = Team.objects.get_or_create(
                        name=team_data['team']['name'],
                        defaults={'crest': team_data['team']['crest'], 
                                  'short_name': team_data['team'].get('shortName', '')}
                    )

                    # Update or create participation record
                    TeamParticipation.objects.update_or_create(
                        team=team,
                        league=league,
                        defaults={
                            'position': team_data['position'],
                            'playedGames': team_data['playedGames'],
                            'won': team_data['won'],
                            'draw': team_data['draw'],
                            'lost': team_data['lost'],
                            'points': team_data['points'],
                            'goalDifference': team_data['goalDifference']
                        }
                    )

                self.stdout.write(self.style.SUCCESS(f'Standings for {name} updated successfully!'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to fetch standings for {name}'))
