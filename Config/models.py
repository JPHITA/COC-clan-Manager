from django.db import models

# Create your models here.

class Constantes(models.Model):
    nombre = models.CharField(max_length=50)
    valor = models.TextField(blank=True)