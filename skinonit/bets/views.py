from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserBet, Bet
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'bets/index.html')

def create_bet(request):
    name = request.POST['name']
    description = request.POST['description']
    bet = Bet(name=name, description=description, win=None)
    bet.save()
    print(bet.id)
    return render(request, 'bets/bet_wager.html', {'bet': bet})

def wager_bet(request):
    # ammount = request.POST['ammount']
    # for_against = request.POST['for_against']
    return render(request, 'bets/bet_wager.html')



