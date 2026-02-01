from django.db import models
from django.contrib.auth.models import User

class Perro(models.Model):
    nombre = models.CharField(max_length=100)
    raza = models.CharField(max_length=100)
    edad = models.IntegerField()
    propietario = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='perros')
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre
    