from django.db import models
from perros.models import Perro

class Entrenamiento(models.Model):
    TIPOS_ENTRENAMIENTO = [
        ('Nivel 1', 'Obediencia básica'),
        ('Nivel 2', 'Control Avanzado'),
        ('Nivel 3', 'Entrenamiento de deportivo'),
        ('SO', 'Sociabilización'),
    ]

    perro = models.ForeignKey(Perro, on_delete=models.CASCADE, related_name='entrenamientos')
    tipo = models.CharField(max_length=10, choices=TIPOS_ENTRENAMIENTO)
    fecha = models.DateField()
    duracion = models.IntegerField(help_text="Duración en minutos")
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.perro.nombre}"