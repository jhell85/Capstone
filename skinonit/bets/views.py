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

def outcome_page(request):
    rows = []
    open_bets = []
    for bet in Bet.objects.filter(win=None):
        row = {
        'name' : bet.name,
        'description' : bet.description,
        'id' : bet.id
        }
        open_bets.append(bet)
        rows.append(row)
    print(rows)
    return render(request,'bets/outcome_page.html', {'rows': rows})    

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
    amount = int(request.POST['amount'])
    print('\n'*25, type(amount), '\n'*25)
    for_against = request.POST['for_against']
    bet = request.POST['bet']

    # update the user's credits
    user_profile = request.user.userprofile
    user_profile.credits -= amount
    user_profile.save()


    # user_credits = user_profile.credits
    ## user_credits = request.user.userprofile.credits #(why does this work what is it getting)
    # new_credits = (user_credits) - int(amount)
    # user_profile.credits = new_credits
    #user_profile.save()
    

    userbet = UserBet(userprofile=userprofile, amount=amount, for_against=for_against, bet_id=bet)
    userbet.save() 
    
    url = reverse('bets:complete_page', kwargs={'bet_id': userbet.id})#why if bet_id changes to userbet_id it fails?
    # if for_against != (True):
    #     return HttpResponseRedirect(reverse('bets:wager_bet'))
    # return HttpResponseRedirect(url)
    return HttpResponseRedirect(url)

def bet_outcome(request):
    win = request.POST['win']
    bet_id = int(request.POST['bet_id'])
    bet = Bet(pk=bet_id, win=win)
    print(f'------------------{bet}------------------------')
    bet.save()

    return render(request,'bets/outcome_page.html')