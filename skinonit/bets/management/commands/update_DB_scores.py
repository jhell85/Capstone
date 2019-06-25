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
yesterday = (datetime.datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
yesterday2 = (datetime.datetime.now() - timedelta(1)).strftime('%Y' + '%m' + '%d')
print(yesterday)
class Command(BaseCommand):
    def handle(self, *args, **options):
        r = requests.get(  
            url='https://api.mysportsfeeds.com/v1.2/pull/nba/current/scoreboard.json?fordate='+ yesterday2,
            headers={
                "Authorization": "Basic " + base64.b64encode(f'{mysportsfeeds_api_key}:{mysportsfeeds_password2}'.encode('utf-8')).decode('ascii')
            }
        )
        apigames = json.loads(r.text)['scoreboard']['gameScore']

now = pytz.utc.localize(datetime.datetime.utcnow())
games=Game.objects.filter(date= yesterday)
for g in games:
    print(g)

