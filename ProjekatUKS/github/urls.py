from django.urls import path

from . import views

app_name = 'github'
urlpatterns = [
    path('', views.home, name='home'),
    path('registration', views.registration, name='registration'),
    path('saveUser', views.saveUser, name='saveUser'),
    path('activate_user/<username>', views.activate_user, name='activate_user'),
    path('login', views.login, name='login'),
]