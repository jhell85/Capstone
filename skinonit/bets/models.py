from django.db import models
from users.models import UserProfile

class Bet(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    win = models.BooleanField(default=None, null=True, blank=True)
    def __str__(self):
        return f'{self.name} - Description: {self.description} open: {self.win}'
class UserBet(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.PROTECT)
    bet = models.ForeignKey(Bet, on_delete=models.PROTECT)
    ammount = models.IntegerField()
    for_against = models.BooleanField()
    def __str__(self):
        return f'{self.bet.name} - {self.ammount} - side of bet:{self.for_against} {self.user.user.username}'
