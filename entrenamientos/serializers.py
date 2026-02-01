from rest_framework import serializers
from .models import Entrenamiento

class EntrenamientoSerializer(serializers.ModelSerializer):
    perro_nombre = serializers.CharField(
        source='perro.nombre',
        read_only=True
    )

    class Meta:
        model = Entrenamiento
        fields = [
            'id',
            'perro',
            'perro_nombre',
            'tipo',
            'fecha',
            'duracion',
            'observaciones'
        ]