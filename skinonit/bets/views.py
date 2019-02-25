from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserBet, Bet
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



# /bet/ - index, create a bet
# /bet/<int:bet_id>/ - create a wager for bet with id bet_id

@login_required
def index(request):
    return render(request, 'bets/index.html')

def wager_page(request, bet_id):
    bet = Bet.objects.get(id=bet_id)
    return render(request, 'bets/bet_wager.html',{'bet': bet})

def complete_page(request, bet_id):
    user_bet = UserBet.objects.get(id=bet_id)
    print('\n'*25, user_bet)
    return render(request, 'bets/complete_page.html',{'user_bet': user_bet})

def create_bet(request):
    name = request.POST['name']
    description = request.POST['description']
    bet = Bet(name=name, description=description, win=None)
    bet.save()
    print(bet.id)
    # change to httpresponseredirect, make another view to render the template
    # return render(request, 'bets/bet_wager.html', {'bet': bet})
    url = reverse('bets:wager_page', kwargs={'bet_id': bet.id})
    return HttpResponseRedirect(url)

def wager_bet(request):
    user = request.user.id
    amount = request.POST['amount']#why does this come through as a string?
    print('\n'*25, type(amount), '\n'*25)
    for_against = request.POST['for_against']
    bet = request.POST['bet'] 
    user_profile = UserProfile.objects.get(pk=user)
    user_credits = user_profile.credits
 # user_credits = request.user.userprofile.credits #(why does this work what is it getting)
    new_credits = (user_credits) - int(amount)
    
    user_profile.credits = new_credits
    user_profile.save()
    

    userbet = UserBet(user_id=user,ammount=amount, for_against=for_against, bet_id=bet)
    userbet.save() 
    
    url = reverse('bets:complete_page', kwargs={'bet_id': userbet.id})#why if bet_id changes to userbet_id it fails?
    # if for_against != (True):
    #     return HttpResponseRedirect(reverse('bets:wager_bet'))
    # return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)

