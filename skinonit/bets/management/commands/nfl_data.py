from django.core.management.base import BaseCommand
import requests
import base64
import json
import datetime
from datetime import timedelta
from bets.models import SportBet, FutureBet
from .secrets import mysportsfeeds_api_key, mysportsfeeds_password

'''
this program is made to grab the data from the api that includes the information of all the games 
played for the season and bring it into the models data base 
'''

yesterday = (datetime.datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
yesterday2 = (datetime.datetime.now() - timedelta(1)).strftime('%Y' + '%m' + '%d')

date = yesterday2
print(date)
class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get(
            
            url='https://api.mysportsfeeds.com/v2.1/pull/nfl/2019-regular/date/'+date+'/odds_futures.json',
            # url='https://api.mysportsfeeds.com/v2.1/pull/mlb/current/date/'+date+'/odds_futures.json',

            # url = 'https://api.mysportsfeeds.com/v1.2/pull/nba/current/full_game_schedule.json',
            # url='https://api.mysportsfeeds.com/v1.2/pull/nba/current/scoreboard.json?fordate='+ date,
            headers={
                "Authorization": "Basic " + base64.b64encode(f'{mysportsfeeds_api_key}:{mysportsfeeds_password}'.encode('utf-8')).decode('ascii')
            }
        )

        # gets latest FuturesBet odds data from api
        futures = json.loads(r.text)['futures']
        for b in futures:
            furturedescription = b['futureDescription'] # getting the bet description
            betupdate = b['lineHistory'][-1]['asOfTime']
            source = b['source']['name']
            for line in b['lineHistory'][-1]['lines']:
                futurebet = FutureBet()
                futurebet.league = 'NFL'
                futurebet.updated = betupdate
                futurebet.description = furturedescription
                futurebet.team = line['lineDescription']
                futurebet.american = line['line']['american']
                futurebet.decimal = line['line']['decimal']
                futurebet.fractional = line['line']['fractional']
                futurebet.source = source
                # futurebet.save()
                print(futurebet)
