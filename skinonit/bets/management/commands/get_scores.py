from django.core.management.base import BaseCommand
import requests
import base64
import json
import datetime
from datetime import timedelta
from bets.models import SportBet
from .secrets import mysportsfeeds_api_key, mysportsfeeds_password

yesterday = (datetime.datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
yesterday2 = (datetime.datetime.now() - timedelta(1)).strftime('%Y' + '%m' + '%d')
print(yesterday)
class Command(BaseCommand):
    def handle(self, *args, **options):
        r = requests.get(  
            url='https://api.mysportsfeeds.com/v1.2/pull/nba/current/scoreboard.json?fordate='+ yesterday2,
            headers={
                "Authorization": "Basic " + base64.b64encode(f'{mysportsfeeds_api_key}:{mysportsfeeds_password}'.encode('utf-8')).decode('ascii')
            }
        )
        games = json.loads(r.text)['scoreboard']['gameScore']
        
        bets = SportBet.objects.filter(eventdate= yesterday)
        for b in bets:
            print()
            print("+++++")
            print(b.idofapi)
            for api in games:
                print('   ' + api['game']['ID'])
                if int(api['game']['ID']) == int(b.idofapi):
                    print('match')
                    b.awayscore = api['awayScore']
                    b.homescore = api['homeScore']
                    b.completed = True
                    b.save()
