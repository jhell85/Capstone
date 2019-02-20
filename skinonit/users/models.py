from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    username = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    credits = models.IntegerField()

    def __str__(self):
        return self.username
