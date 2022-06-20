import email
from django.db import models

# Create your models here.

class Utente(models.Model):
    nome = models.CharField(max_length=20)
    cognome = models.CharField(max_length=20)
    email = models.CharField(max_length=40, unique=True)
    password = models.CharField(max_length=127)
    iban = models.CharField(max_length=27, unique=True)
    foto = models.CharField(max_length=20, default="default.png")
    euro = models.FloatField()
    dollari = models.FloatField()

class Transizione(models.Model):
    fk_utente = models.ForeignKey(Utente, on_delete=models.CASCADE)
    quantita_spesa = models.FloatField()
    quantita_comprata = models.FloatField()
    valuta_comprata = models.CharField(max_length=3)
    data = models.DateField()