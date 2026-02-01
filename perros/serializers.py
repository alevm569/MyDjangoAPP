from rest_framework import serializers
from .models import Perro

class PerroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perro
        fields = '__all__'