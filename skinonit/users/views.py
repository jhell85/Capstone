from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
     next = request.GET.get('next', '')
     return render(request, 'users/index.html', {'next': next})

def register_user(request):
    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    confirm_password = request.POST['confirm_password']
    next = request.POST['next']

    user = User.objects.create_user(username, email, password)
    login(request, user)
    credits = 500.00

    # create user profile with 100 credits to start

    if next == '':
        return HttpResponseRedirect(reverse('users:protected'))
    return HttpResponseRedirect(next)

@login_required
def protected(request):
    return render(request, 'users/protected.html')

def login_user(request):
    username = request.POST['username']
    password = request.POST['password']
    next = request.POST['next']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        if next == '':
            return HttpResponseRedirect(reverse('users:protected'))
        return HttpResponseRedirect(next)
    return HttpResponseRedirect(reverse('users:index'))
