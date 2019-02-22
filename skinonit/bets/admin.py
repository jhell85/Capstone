from django.contrib import admin

from .models import Bet, UserBet

admin.site.register(Bet)
admin.site.register(UserBet)
