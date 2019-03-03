from django.core.management.base import BaseCommand
import requests
import base64
import json
import datetime
from bets.models import SportBet
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
            completed = True if (game['isCompleted']) == 'true' else False
            sportbet = SportBet()
            sportbet.homecity = game['game']['homeTeam']['City']
            sportbet.hometeam = game['game']['homeTeam']['Name']
            sportbet.awaycity = game['game']['awayTeam']['City']
            sportbet.awayteam = game['game']['awayTeam']['Name']
            sportbet.eventdate = game['game']['date']
            sportbet.homescore = game['homeScore']
            sportbet.awayscore = game['awayScore']
            sportbet.completed = completed
            sportbet.idofapi = game['game']['ID']

            print(sportbet.completed)
            sportbet.save()
            
            
            
            print(sportbet.eventdate)
        
