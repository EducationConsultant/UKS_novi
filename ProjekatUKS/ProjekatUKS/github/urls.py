from django.urls import path

from . import views

app_name = 'github'
urlpatterns = [
    path('', views.pocetna, name='pocetna'),
    path('registracija', views.registracija, name='registracija'),
    path('registrujKorisnika', views.registrujKorisnika, name='registrujKorisnika'),
]