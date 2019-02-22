from django.urls import path
from . import views

app_name = 'bets'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_bet', views.create_bet, name='create_bet'),
]

