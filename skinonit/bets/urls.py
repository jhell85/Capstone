from django.urls import path
from . import views

app_name = 'bets'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_bet', views.create_bet, name='create_bet'),
    path('wager_bet', views.wager_bet, name='wager_bet'),
    path('wager_page/<int:bet_id>', views.wager_page, name='wager_page'),
    path('complete_page/<int:bet_id>', views.complete_page, name='complete_page'),
]

