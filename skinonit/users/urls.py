from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    path('register_user/', views.register_user, name='register_user'),
    path('protected/', views.protected, name='protected'),
    path('login_user', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('login_page/', views.login_page, name='login_page'),
]