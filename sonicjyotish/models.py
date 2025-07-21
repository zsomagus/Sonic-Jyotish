from django.db import models


class Elemzes(models.Model):
    vezetek_nev = models.CharField(max_length=50)
    kereszt_nev = models.CharField(max_length=50)
    datum = models.DateField()
    ido = models.TimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    ido_zona = models.CharField(max_length=20)
    nyari_idoszamitas = models.BooleanField(default=False)
    varga = models.CharField(max_length=20)
    letrehozva = models.DateTimeField(auto_now_add=True)
