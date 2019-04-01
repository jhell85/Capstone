from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserBet, Bet, SportBet, UserSportBet, FutureBet
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from datetime import timedelta
from django.core import management
from django.core.management import call_command
from django.core.management.commands import loaddata
from bets.management.commands.secrets import mysportsfeeds_api_key, mysportsfeeds_password
from django.core.management.base import BaseCommand
import requests
import base64
import json
import datetime
from datetime import timedelta
from bets.models import SportBet
# from secrets import mysportsfeeds_api_key, mysportsfeeds_password
def api_date(n):
    return (datetime.datetime.now() - timedelta(n)).strftime('%Y' + '%m' + '%d')
def get_date(n):
   return (datetime.datetime.now() + timedelta(n)).strftime('%Y-%m-%d')
def get_date_text(n):
    return (datetime.datetime.now() + timedelta(n)).strftime('%a %b %d')

def get_updatedodds():
    r = requests.get(
                url='https://api.mysportsfeeds.com/v2.1/pull/nba/2018-2019-regular/date/'+api_date(1)+'/odds_futures.json?source=bovada',
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
                        futurebet.save()
                        print(f'--------------------{api_team} ---- {bet.team}')
        print('program ran')
def get_open_bets():
    rows = []
    for bet in Bet.objects.filter(win__isnull=True):
        row = {
            'name' : bet.name,
            'description' : bet.description,
            'id' : bet.id
        }
        rows.append(row)
    return rows

def get_open_sportbets():
    games = []
    # tomorrow = (datetime.datetime.now() + timedelta(1)).strftime('%Y-%m-%d')
    # tomorrow2 = (datetime.datetime.now() + timedelta(1)).strftime('%a %b %d')
    
    for x in range(0, 4):
        
        date = get_date(x)
        text_date = get_date_text(x)
        for bet in SportBet.objects.filter(eventdate=date):

            game = {
                'date' : text_date,
                'id' : bet.id,
                'homecity' : bet.homecity,
                'hometeam' : bet.hometeam,
                'awaycity' : bet.awaycity,
                'awayteam' : bet.awayteam,
            }
            games.append(game)
            x =+ 1
    get_open_futureodds()
    return games
def get_open_futureodds():
    get_updatedodds()
    bet_lines = []
    bets = FutureBet.objects.all()
    counter = 0
    for bet in bets: 
        future = {
            'description' : bet.description,
            'id' : bet.id,
            'team' : bet.team,
            'fractional' : bet.fractional,
            'counter' : counter
        }
        counter += 1
        bet_lines.append(future)
    return bet_lines

    

def create_usersportbet(request):
    bet_id = request.POST['sportbet_id']
    print(10*'-')
    print(bet_id)
    print(10*'-')
    url = reverse('bets:sportwager_page', kwargs={'bet_id': bet_id})
    return HttpResponseRedirect(url)

def sportwager_page(request, bet_id):
    bet = SportBet.objects.get(id=bet_id)
    return render(request, 'bets/sportbet_wager.html',{'bet': bet})

@login_required
def index(request):
    return render(request, 'bets/index.html')

@login_required
def wager_page(request, bet_id):
    bet = Bet.objects.get(id=bet_id)
    return render(request, 'bets/bet_wager.html',{'bet': bet})

@login_required
def complete_page(request, bet_id):
    user_bet = UserBet.objects.get(id=bet_id)
    print('\n'*25, user_bet)
    return render(request, 'bets/complete_page.html',{'user_bet': user_bet})

def complete_sportpage(request, bet_id):
    user_bet = UserSportBet.objects.get(id=bet_id)
    return render(request, 'bets/complete_sportpage.html',{'user_bet': user_bet})

@login_required
def outcome_page(request):
    rows = get_open_bets()
    return render(request,'bets/outcome_page.html', {'rows': rows})  

@login_required
def openbets_page(request):
    tomorrow = (datetime.datetime.now() + timedelta(1)).strftime('%x')
    rows = get_open_bets()
    games = get_open_sportbets()
    futures = get_open_futureodds()
    return render(request, 'bets/openbets_page.html', {'rows': rows, 'games': games, 'tomorrow': tomorrow, 'futures': futures})

def create_userbet(request):
    bet_id = request.POST['bet_id']
    url = reverse('bets:wager_page', kwargs={'bet_id': bet_id})
    return HttpResponseRedirect(url)

def create_bet(request):
    name = request.POST['name']
    description = request.POST['description']
    bet = Bet(name=name, description=description, win=None)
    bet.save()
    # change to httpresponseredirect, make another view to render the template
    # return render(request, 'bets/bet_wager.html', {'bet': bet})
    url = reverse('bets:wager_page', kwargs={'bet_id': bet.id})
    return HttpResponseRedirect(url)

def sportwager_bet(request):
    amount = int(request.POST['amount'])
    home = request.POST['home']
    bet = request.POST['bet']
    user_profile = request.user.userprofile
    user_profile.credits -= amount
    user_profile.save()
    userbet = UserSportBet(userprofile=user_profile, amount=amount, home=home, sportbet_id=bet)
    userbet.save() 
    url = reverse('bets:complete_sportpage', kwargs={'bet_id': userbet.id})
    return HttpResponseRedirect(url)


def wager_bet(request):
    amount = int(request.POST['amount'])
    for_against = request.POST['for_against']
    bet = request.POST['bet']
    # update the user's credits
    user_profile = request.user.userprofile
    user_profile.credits -= amount
    user_profile.save()
    print('\n'*25, user_profile, '\n'*25)
    userbet = UserBet(userprofile=user_profile, amount=amount, for_against=for_against, bet_id=bet)
    userbet.save() 
    url = reverse('bets:complete_page', kwargs={'bet_id': userbet.id})#why if bet_id changes to userbet_id it fails?
    #     return HttpResponseRedirect(reverse('bets:wager_bet'))
    # return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)

def bet_outcome(request):
    win = request.POST['win']
    win = True if win == 'True' else False
    bet_id = int(request.POST['bet_id'])
    bet = Bet.objects.get(id=bet_id)
    bet.win = win
    # bet.save()
    for user_bet in bet.userbet_set.all():# UserBet.objects.filter(bet_id=bet_id):(this is the same thing as the code but grabbing it in a different way)
        if user_bet.for_against == bet.win:
            user_bet.userprofile.credits += user_bet.amount*2
            user_bet.userprofile.save() 
        # if the bet's 'win' equals the userbet's 'win' pay out the userprofile
        # add the credits to the user profile and save it
    return HttpResponseRedirect(reverse('bets:outcome_page'))

def scores_page(request):
    return render(request, 'bets/scores_page.html')