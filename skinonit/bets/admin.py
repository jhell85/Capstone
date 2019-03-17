from django.contrib import admin

from .models import Bet, UserBet, SportBet, UserSportBet, FutureBet

admin.site.register(Bet)
admin.site.register(UserBet)
admin.site.register(SportBet)
admin.site.register(UserSportBet)
admin.site.register(FutureBet)