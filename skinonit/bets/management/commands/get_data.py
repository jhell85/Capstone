from django.core.management.base import BaseCommand
import requests
import base64
import json
import datetime
from datetime import timedelta
from bets.models import SportBet, FutureBet, Game
from .secrets import mysportsfeeds_api_key, mysportsfeeds_password2, mysportsfeeds_password

'''
this program is made to grab the data from the api that includes the information of all the games 
played for the season and bring it into the models data base 
'''

yesterday = (datetime.datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
yesterday2 = (datetime.datetime.now() - timedelta(1)).strftime('%Y' + '%m' + '%d')

date = yesterday2
class Command(BaseCommand):

    def handle(self, *args, **options):
        r = requests.get(
            
            # url='https://api.mysportsfeeds.com/v2.1/pull/nba/2018-2019-regular/date/'+date+'/odds_gamelines.json?source=bovada',
            # url='https://api.mysportsfeeds.com/v2.1/pull/nba/2018-2019-regular/date/'+date+'/odds_futures.json?source=bovada',

            # url = 'https://api.mysportsfeeds.com/v1.2/pull/nba/current/full_game_schedule.json',
            # url='https://api.mysportsfeeds.com/v1.2/pull/nba/current/scoreboard.json?fordate='+ date,
            url='https://api.mysportsfeeds.com/v1.1/pull/mlb/2019-regular/full_game_schedule.json',
            headers={
                "Authorization": "Basic " + base64.b64encode(f'{mysportsfeeds_api_key}:{mysportsfeeds_password2}'.encode('utf-8')).decode('ascii')
            }
        )

        # gets latest FuturesBet odds data from api
        # futures = json.loads(r.text)['futures']
        # for b in futures:
        #     furturedescription = b['futureDescription']
        #     betupdate = b['lineHistory'][-1]['asOfTime']
        #     for line in b['lineHistory'][-1]['lines']:
        #         futurebet = FutureBet()
        #         futurebet.league = 'NBA'
        #         futurebet.updated = betupdate
        #         futurebet.description = furturedescription
        #         futurebet.team = line['lineDescription']
        #         futurebet.american = line['line']['american']
        #         futurebet.decimal = line['line']['decimal']
        #         futurebet.fractional = line['line']['fractional']
        #         # futurebet.save()
        #         print(futurebet)


       

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



        games = json.loads(r.text)['fullgameschedule']['gameentry']
       
        for v in games:
            date = v['date']
            gamedate = datetime.datetime.strptime(date, '%Y-%m-%d')
            if gamedate > datetime.datetime.now():
                game = Game()
                game.date = date
                game.time = v['time']
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
        #     # completed = True if (game['isCompleted']) == 'true' else False
        #     sportbet = SportBet()
        #     sportbet.homecity = game['game']['homeTeam']['City']
        #     sportbet.hometeam = game['game']['homeTeam']['Name']
        #     sportbet.awaycity = game['game']['awayTeam']['City']
        #     sportbet.awayteam = game['game']['awayTeam']['Name']
        #     sportbet.eventdate = game['game']['date']
        #     sportbet.homescore = game['homeScore']
        #     sportbet.awayscore = game['awayScore']
        #     sportbet.completed = True#completed
        #     sportbet.idofapi = game['game']['ID']
        #     print(sportbet)
        # #     sportbet.save()
            
            
            
            
        
