from django.core.management.base import BaseCommand
import requests
import base64
import json
import datetime
from .secrets import mysportsfeeds_api_key, mysportsfeeds_password


class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get(
            url='https://api.mysportsfeeds.com/v1.2/pull/nba/current/scoreboard.json?fordate=20190228',
            headers={
                "Authorization": "Basic " + base64.b64encode(f'{mysportsfeeds_api_key}:{mysportsfeeds_password}'.encode('utf-8')).decode('ascii')
            }
        )
        games = json.loads(r.text)['scoreboard']['gameScore']
        for game in games:
            print(game['awayScore'])
        
