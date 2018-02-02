from django.shortcuts import render

from github.models import Korisnik


def pocetna(requset):
    return render(requset, 'github/pocetna.html')

def registracija(request):
    return render(request, 'github/registracija.html')

def registrujKorisnika(request):
    korisnickoIme = request.POST['korisnickoIme']

    ime = request.POST['ime']
    prezime = request.POST['prezime']
    lozinka = request.POST['lozinka']
    emailAdresa = request.POST['emailAdresa']

    korisnik = Korisnik()
    korisnik.ime = ime
    korisnik.prezime = prezime
    korisnik.korisnickoIme = korisnickoIme
    korisnik.lozinka = lozinka
    korisnik.emailAdresa = emailAdresa

    korisnik.save()

    return render(request, 'github/pocetna.html')