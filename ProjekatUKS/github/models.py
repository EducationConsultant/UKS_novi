from django.db import models


# Create your models here.
class Korisnik(models.Model):
    ime = models.CharField(max_length=50)
    prezime = models.CharField(max_length=80)
    korisnickoIme = models.CharField(max_length=20)
    lozinka = models.CharField(max_length=50)
    emailAdresa = models.CharField(max_length=50)

    def __str__(self):
        return self.ime + " " + self.prezime + " " + self.korisnickoIme + " " + self.emailAdresa
