from django.urls import path
from . import views

app_name = 'bets'
urlpatterns = [
    path('', views.index, name='index'),
    path('create_bet', views.create_bet, name='create_bet'),
    path('wager_bet', views.wager_bet, name='wager_bet'),
    path('wager_page/<int:bet_id>', views.wager_page, name='wager_page'),
    path('complete_page/<int:bet_id>', views.complete_page, name='complete_page'),
    path('bet_outcome', views.bet_outcome, name='bet_outcome'),
    path('outcome_page', views.outcome_page, name='outcome_page'),
    path('create_userbet', views.create_userbet, name='create_userbet'),
    path('openbets_page', views.openbets_page, name='openbets_page'),
    path('scores_page', views.scores_page, name='scores_page'),
    path('create_usersportbet', views.create_usersportbet, name='create_usersportbet'),
]

