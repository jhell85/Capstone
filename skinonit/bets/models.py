from django.db import models
from users.models import UserProfile
from fractions import Fraction

class Bet(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    win = models.BooleanField(default=None, null=True, blank=True)
    def __str__(self):
        return f'{self.name} - Description: {self.description} open: {self.win}'

class UserBet(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    bet = models.ForeignKey(Bet, on_delete=models.PROTECT)
    amount = models.IntegerField()
    for_against = models.BooleanField()
    def __str__(self):
        return f'{self.bet.name} - {self.amount} - side of bet:{self.for_against} {self.userprofile.user.username}'
    def for_against_name(self):
        if self.for_against == True:
            return f'for'
        else:
            return f'against'
    def payout(self):
        payout = ((self.amount) *2)
        return payout


class SportBet(models.Model):
    hometeam = models.CharField(max_length=200)
    homecity = models.CharField(max_length=200)
    awayteam = models.CharField(max_length=200)
    awaycity = models.CharField(max_length=200)
    eventdate = models.DateField()
    homescore = models.IntegerField(default=0)
    awayscore = models.IntegerField(default=0)
    completed = models.BooleanField()
    idofapi = models.IntegerField(default=None)
    league = models.CharField(max_length=100)
    source = models.CharField(max_length=100)

    def __str__(self):
        if self.completed == True:
            return f'{self.eventdate} {self.awayteam} {self.awayscore} @ {self.hometeam} {self.homescore}'
        else:
            return f'{self.eventdate} {self.awayteam} @ {self.hometeam} completed: {self.completed}'

class UserSportBet(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    sportbet = models.ForeignKey(SportBet, on_delete=models.PROTECT)
    home = models.BooleanField()
    amount = models.IntegerField()
    odds = models.FloatField(default=1.0)

    def __str__(self):
        return f'{self.sportbet} {self.userprofile} amount:{self.amount} home:{self.home}'
    
    def user_team(self):
        if self.home:
            return self.sportbet.hometeam
        return self.sportbet.awayteam

    def user_city(self):
        if self.home:
            return self.sportbet.homecity
        return self.sportbet.awaycity

    def opponet_city(self):
        if self.home:
            return self.sportbet.awaycity
        return self.sportbet.homecity

    def opponet_team(self):
        if self.home:
            return self.sportbet.awayteam
        return self.sportbet.hometeam

    def home_away(self):
        if self.home:
            return 'at home'
        return 'on the road'

    def eventdate(self):
        return self.sportbet.eventdate

    def payout(self):
        return self.amount*2
    

class FutureBet(models.Model):
    league = models.CharField(max_length=10)
    updated = models.DateTimeField()
    description = models.CharField(max_length=200)
    team = models.CharField(max_length=200)
    american = models.IntegerField(default=0)
    decimal = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    fractional = models.CharField(max_length=10)
    source = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.updated}-{self.description} - {self.team} - {self.fractional} - {self.source}'
    