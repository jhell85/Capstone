from django.db import models
from django.contrib.auth.models import User

class Bet(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    win_loss = models.BooleanField(default=None)

class UserBet(models.Model):
     user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
     bet = models.ForeignKey(Bet, on_delete=models.PROTECT)
     ammount = models.IntegerField()
     for_against = models.BooleanField()

