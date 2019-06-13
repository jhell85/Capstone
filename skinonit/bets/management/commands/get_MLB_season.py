from django.core.management.base import BaseCommand
import requests
import base64
import json
import datetime
import pytz
from datetime import timedelta
from bets.models import  Game
from .secrets import mysportsfeeds_api_key, mysportsfeeds_password2
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
        for v in games:
            time = (v['time'])
            date = (v['date'])
            date_time = f'{date}-{time}'
            timezone = pytz.timezone('US/Eastern')
            gamedate = datetime.datetime.strptime(date_time, '%Y-%m-%d-%I:%M%p') 
            gamedate_aware = gamedate.astimezone(pytz.timezone("America/Los_Angeles"))
            now = pytz.utc.localize(datetime.datetime.utcnow())

            print (f'{now}----{gamedate_aware}')
            if gamedate_aware > now:
                game = Game()
                game.date = gamedate
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
                # game.save()