from django.core.management.base import BaseCommand
import requests
import base64
import json
import datetime
import time
from datetime import timedelta
from bets.models import SportBet, FutureBet
from .secrets import mysportsfeeds_api_key, mysportsfeeds_password

tomorrow = (datetime.datetime.now() - timedelta(1)).strftime('%Y' + '%m' + '%d')
class Command(BaseCommand):
    def handle(self, *args, **options):
        r = requests.get(
            url='https://api.mysportsfeeds.com/v2.1/pull/nba/2018-2019-regular/date/'+tomorrow+'/odds_futures.json?source=bovada',
            headers={
                "Authorization": "Basic " + base64.b64encode(f'{mysportsfeeds_api_key}:{mysportsfeeds_password}'.encode('utf-8')).decode('ascii')
            }
        )
        futures = json.loads(r.text)['futures']
        # going through the lines from the api
        for api_bet in futures:
            furturedescription = api_bet['futureDescription']
            betupdate = datetime.datetime.strptime(api_bet['lineHistory'][-1]['asOfTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
            #getting the date time of the api and converting it to a datetime format to compare with the data base
            bets = FutureBet.objects.filter(description=furturedescription)
            bet_list =[]
            for bet in bets: # creating a list to check later in the loop
                bet_list.append(f'{bet.team}')
            for bet in bets: # looping through all bets in Models
                if betupdate > (bet.updated).replace(tzinfo=None): # comparing the time they were last updated to the time in the Modles
                    # print(f'update {bet.description} {bet.team}')
                    # print(bet_list)
                    for line in api_bet['lineHistory'][-1]['lines']: #looping through newest list of bet lines from the API
                        api_team = line['lineDescription']
                        print(f'Models --{bet.team}')
                        print(f'API --{api_team}')
                        if api_team == bet.team: #finding a matching team to update
                            bet.american = line['line']['american']
                            bet.decimal = line['line']['decimal']
                            bet.fractional = line['line']['fractional']
                            bet.updated = betupdate
                            bet.save()
                            print (line)
                            print(bet)
                        if api_team not in bet_list:                          
                            futurebet = FutureBet()
                            futurebet.league = 'NBA'
                            futurebet.updated = betupdate
                            futurebet.description = furturedescription
                            futurebet.team = line['lineDescription']
                            futurebet.american = line['line']['american']
                            futurebet.decimal = line['line']['decimal']
                            futurebet.fractional = line['line']['fractional']
                            # futurebet.save()
                            print(f'--------------------{api_team} ---- {bet.team}')
            print('program ran')