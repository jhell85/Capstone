from django.core.management.base import BaseCommand
import requests
import base64
import json
import datetime
from datetime import timedelta
from bets.models import SportBet
from .secrets import mysportsfeeds_api_key, mysportsfeeds_password
'''
This program is made to grab the scores of the games that happened yesterday update the games in the model's
data base then then find which team won and compares that to each userbet that was created from the game 
if the player picked the winning team it pays out the credits to the user's profile,
if the user picked the incorrect team it does nothing
'''

yesterday = (datetime.datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
yesterday2 = (datetime.datetime.now() - timedelta(1)).strftime('%Y' + '%m' + '%d')
print(yesterday)
class Command(BaseCommand):
    def handle(self, *args, **options):
        r = requests.get(  
            url='https://api.mysportsfeeds.com/v1.2/pull/nba/current/scoreboard.json?fordate='+ yesterday2,
            headers={
                "Authorization": "Basic " + base64.b64encode(f'{mysportsfeeds_api_key}:{mysportsfeeds_password}'.encode('utf-8')).decode('ascii')
            }
        )
        games = json.loads(r.text)['scoreboard']['gameScore']
        
        bets = SportBet.objects.filter(eventdate= yesterday)
        for b in bets: # going through all the games from yesterday in my data base
            print()
            print("+++++")
            print(b.idofapi)
            for api in games: # going through all the games for yesterday from the API
                print('   ' + api['game']['ID'])
                if int(api['game']['ID']) == int(b.idofapi): # finding a match for the API and my data base
                    print('match')
                    b.awayscore = api['awayScore']
                    b.homescore = api['homeScore']
                    b.completed = True
                    b.save() # updating the scores in the data base with the scores from the API
                    for userbet in b.usersportbet_set.all(): #getting all the usersbets that are asociated the sportbet
                        print("whhhhhaaaaatttt")     
                        print(userbet.userprofile.credits)
                        homescore = None #setting homescore to true if the home team won else false
                        if b.homescore > b.awayscore:
                            homescore = True
                        else:
                            homescore = False
                        print(homescore)
                        #if homescore is true and the user picked home then pay out the user or awayteam won and user picked away pay out the user
                        if homescore == userbet.home:
                            userbet.userprofile.credits += (userbet.amount*2)
                            userbet.save()
                            userbet.userprofile.save()
                            print(userbet.userprofile.credits)




                        

