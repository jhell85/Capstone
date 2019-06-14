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
        if counter < 15:
            for v in games:
                time = v['time']
                date = v['date']
                date_time = f'{date}-{time}'
                timezone = pytz.timezone('US/Eastern')
                # gamedate = pytz.utc.localize(datetime.datetime.strptime(date_time, '%Y-%m-%d-%I:%M%p')) 
                # gamedate_aware = gamedate.astimezone(pytz.timezone("US/Eastern"))
                gamedate_aware = pytz.timezone("US/Eastern").localize(datetime.datetime.strptime(date_time, '%Y-%m-%d-%I:%M%p')).replace(tzinfo=pytz.UTC)
                now = pytz.utc.localize(datetime.datetime.utcnow())
                # now = timezone.localize(datetime.datetime.now())
                print (f'{now}----{gamedate_aware}---{date_time}')
                   
                if gamedate_aware > now:
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
                    counter += 1
                    # game.save()
                    print(counter)
        