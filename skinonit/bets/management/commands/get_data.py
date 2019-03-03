from django.core.management.base import BaseCommand
import requests
import base64
import json
import datetime
from .secrets import mysportsfeeds_api_key, mysportsfeeds_password
def getDate(n):
    x = datetime.datetime.now()
    day = add0(int(x.strftime("%d"))+n)
    month = x.strftime("%m")
    year = x.strftime("%Y")
    return year +''+ month +''+ str(day)
def getYesterday():
    return getDate(-1)

def add0(n):
    if n < 10 :
        return "0" + str(n)
    else :
        return n
    
date = getYesterday()
class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get(
            url='https://api.mysportsfeeds.com/v1.2/pull/nba/current/scoreboard.json?fordate='+ date,
            headers={
                "Authorization": "Basic " + base64.b64encode(f'{mysportsfeeds_api_key}:{mysportsfeeds_password}'.encode('utf-8')).decode('ascii')
            }
        )
        games = json.loads(r.text)['scoreboard']['gameScore']
        for game in games:

            print(game['awayScore'])
        
