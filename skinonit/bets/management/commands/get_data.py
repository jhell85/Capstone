from django.core.management.base import BaseCommand
import requests
import base64
import json
import datetime
from datetime import timedelta
from bets.models import SportBet
from .secrets import mysportsfeeds_api_key, mysportsfeeds_password

'''
this program is made to grab the data from the api that includes the information of all the games 
played for the season and bring it into the models data base 
'''

yesterday = (datetime.datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
yesterday2 = (datetime.datetime.now() - timedelta(0)).strftime('%Y' + '%m' + '%d')

date = yesterday2
class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get(
            url='https://api.mysportsfeeds.com/v2.1/pull/nba/2018-2019-regular/date/'+date+'/odds_gamelines.json?source=bovada',

            # url = 'https://api.mysportsfeeds.com/v1.2/pull/nba/current/full_game_schedule.json',
            # url='https://api.mysportsfeeds.com/v1.2/pull/nba/current/scoreboard.json?fordate='+ date,
            headers={
                "Authorization": "Basic " + base64.b64encode(f'{mysportsfeeds_api_key}:{mysportsfeeds_password}'.encode('utf-8')).decode('ascii')
            }
        )
        games = json.loads(r.text)
        print(games)

        # for game in games:
        #     if game['date'] >= yesterday:
          
        #         sportbet = SportBet()
        #         sportbet.homecity = game['homeTeam']['City']
        #         sportbet.hometeam = game['homeTeam']['Name']
        #         sportbet.awaycity = game['awayTeam']['City']
        #         sportbet.awayteam = game['awayTeam']['Name']
        #         sportbet.eventdate = game['date']
        #         sportbet.homescore = 0
        #         sportbet.awayscore = 0
        #         sportbet.completed = False
        #         sportbet.idofapi = game['id']
        #         print(sportbet)
        #         sportbet.save()



        # games = json.loads(r.text)['scoreboard']['gameScore']
        # for game in games:
        #     completed = True if (game['isCompleted']) == 'true' else False
        #     sportbet = SportBet()
        #     sportbet.homecity = game['game']['homeTeam']['City']
        #     sportbet.hometeam = game['game']['homeTeam']['Name']
        #     sportbet.awaycity = game['game']['awayTeam']['City']
        #     sportbet.awayteam = game['game']['awayTeam']['Name']
        #     sportbet.eventdate = game['game']['date']
        #     sportbet.homescore = game['homeScore']
        #     sportbet.awayscore = game['awayScore']
        #     sportbet.completed = completed
        #     sportbet.idofapi = game['game']['ID']
        #     sportbet.save()
            
            
            
            
        
