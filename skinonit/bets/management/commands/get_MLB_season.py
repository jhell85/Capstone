from django.core.management.base import BaseCommand
import requests
import base64
import json
import datetime
import pytz
from datetime import timedelta
from bets.models import  Game
from .secrets import mysportsfeeds_api_key, mysportsfeeds_password2
from django.utils import timezone
'''
this program is designed to grab the MLB season from the api and put it in the data base  
'''
class Command(BaseCommand):
    def handle(self, *args, **options):
        r = requests.get(
            url='https://api.mysportsfeeds.com/v1.1/pull/mlb/2019-regular/full_game_schedule.json',
            headers={
                "Authorization": "Basic " + base64.b64encode(f'{mysportsfeeds_api_key}:{mysportsfeeds_password2}'.encode('utf-8')).decode('ascii')
            }
        )
        games = json.loads(r.text)['fullgameschedule']['gameentry']
        counter = 0  
        
        for v in games:
            if counter <= 3:
                time = v['time']
                date = v['date']
                event_datetime = f'{date}-{time}'
                gamedate_aware = pytz.timezone("US/Eastern").localize(datetime.datetime.strptime(event_datetime, '%Y-%m-%d-%I:%M%p')).astimezone(pytz.utc)
                # takes the date from the API assigns the timezone EST (because that's what the timezone the games are in from the API) to it then converts that time to UTC time zone to be compared to now 
                G_D = gamedate_aware.strftime('%Y-%m-%d %H:%M:%S %Z')
                now = pytz.utc.localize(datetime.datetime.utcnow())
                now_Z = now.strftime('%Y-%m-%d %H:%M:%S %Z')
                
                
                if gamedate_aware > now:
                    print (f'{now_Z}----{G_D}')
                    game = Game()
                    game.date = gamedate_aware
                    game.idofapi = v['id']
                    game.league = 'MLB'
                    game.completed = False
                    game.hometeam = v['homeTeam']['Name']
                    game.homecity = v['homeTeam']['City']
                    game.awayteam = v['awayTeam']['Name']
                    game.awaycity = v['awayTeam']['City']
                    game.homescore = 0
                    game.awayscore = 0
                    print(game)
                    # counter += 1
                    game.save()
                    print(counter)
        