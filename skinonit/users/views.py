from django.shortcuts import render
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
    return HttpResponseRedirect(next)

    if next == '':
        return HttpResponseRedirect(reverse('users:protected'))
    return HttpResponseRedirect(next)
