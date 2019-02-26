from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserBet, Bet
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

# /bet/ - index, create a bet
# /bet/<int:bet_id>/ - create a wager for bet with id bet_id

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

@login_required
def outcome_page(request):
    rows = get_open_bets()
    return render(request,'bets/outcome_page.html', {'rows': rows})  

@login_required
def openbets_page(request):
    rows = get_open_bets()
    return render(request, 'bets/openbets_page.html', {'rows': rows})

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

def wager_bet(request):
    amount = int(request.POST['amount'])
    
    for_against = request.POST['for_against']
    bet = request.POST['bet']

    # update the user's credits
    user_profile = request.user.userprofile
    user_profile.credits -= amount
    user_profile.save()
    print('\n'*25, user_profile, '\n'*25)

    # user_credits = user_profile.credits
    ## user_credits = request.user.userprofile.credits #(why does this work what is it getting)
    # new_credits = (user_credits) - int(amount)
    # user_profile.credits = new_credits
    #user_profile.save()
    

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
