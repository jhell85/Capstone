from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserBet
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, 'bets/index.html')

def create_bet(request):
    name = request.POST['name']
    discription = request.POST['discription']
    bet = Bet.objects(name=name, ammount=ammount)
    bet.save() 



