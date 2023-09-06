from django.urls import path

from .views import account_register, account_login, account_logout, account_confirm


urlpatterns = [
    path('register/', account_register, name='register'),
    path('confirm/', account_confirm, name='confirm'),
    path('login/', account_login, name='login'),
    path('logout/', account_logout, name='logout'),
]