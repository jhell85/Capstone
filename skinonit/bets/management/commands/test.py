from django.core.management.base import BaseCommand
import requests
import base64
import json
import datetime
import time
from datetime import timedelta
from bets.models import SportBet, FutureBet
from .secrets import mysportsfeeds_api_key, mysportsfeeds_password

bets = FutureBet.objects.filter(description='2018 - 2019 Southwest Division - Odds to Win')

game_dict = []
for b in bets:
    print(f'{b.team}')
#     game = b.team
#     game_dict.append(game)
# print(game_dict)