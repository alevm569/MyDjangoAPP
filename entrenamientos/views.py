from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .serializers import EntrenamientoSerializer
from .models import Entrenamiento
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

class EntrenamientoListView(LoginRequiredMixin, ListView):
    model = Entrenamiento
    template_name = 'perros/entrenamiento_list.html'

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='Administradores').exists():
            return Entrenamiento.objects.all()

        if user.groups.filter(name='Entrenadores').exists():
            return Entrenamiento.objects.all()

        if user.groups.filter(name='Guias').exists():
            return Entrenamiento.objects.filter(perro__propietario=user)

        return Entrenamiento.objects.none()

class EntrenamientoDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Entrenamiento
    template_name = 'perros/entrenamiento_detail.html'

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='Guias').exists():
            return Entrenamiento.objects.filter(perro__propietario=user)

        return Entrenamiento.objects.all()
    
class EntrenamientoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Entrenamiento
    fields = ['perro', 'tipo', 'fecha', 'duracion', 'observaciones']
    success_url = reverse_lazy('entrenamiento-list')

    def test_func(self):
        return self.request.user.groups.filter(
            name__in=['Administradores', 'Entrenadores']
        ).exists()

class EntrenamientoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entrenamiento
    fields = ['perro', 'tipo', 'fecha', 'duracion', 'observaciones']
    success_url = reverse_lazy('entrenamiento-list')

    def test_func(self):
        return self.request.user.groups.filter(
            name__in=['Administradores', 'Entrenadores']
        ).exists()
    
class EntrenamientoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entrenamiento
    success_url = reverse_lazy('entrenamiento-list')

    def test_func(self):
        return self.request.user.groups.filter(name='Administradores').exists() 
    
class EntrenamientoViewSet(ModelViewSet):
    serializer_class = EntrenamientoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='Administradores').exists():
            return Entrenamiento.objects.all()

        if user.groups.filter(name='Entrenadores').exists():
            return Entrenamiento.objects.all()

        if user.groups.filter(name='Guias').exists():
            return Entrenamiento.objects.filter(perro__propietario=user)

        return Entrenamiento.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user

        if user.groups.filter(name__in=['Administradores', 'Entrenadores']).exists():
            serializer.save()
        else:
            raise PermissionError("No tienes permisos para crear entrenamientos")

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def entrenamientos_api(request):
    user = request.user

    # ---- GET ----
    if request.method == 'GET':
        if user.groups.filter(name='Administradores').exists():
            entrenamientos = Entrenamiento.objects.all()

        elif user.groups.filter(name='Entrenadores').exists():
            entrenamientos = Entrenamiento.objects.all()

        elif user.groups.filter(name='Guias').exists():
            entrenamientos = Entrenamiento.objects.filter(
                perro__propietario=user
            )

        else:
            entrenamientos = Entrenamiento.objects.none()

        serializer = EntrenamientoSerializer(entrenamientos, many=True)
        return Response(serializer.data)

    # ---- POST ----
    if request.method == 'POST':
        if not user.groups.filter(
            name__in=['Administradores', 'Entrenadores']
        ).exists():
            return Response(
                {'detail': 'No tienes permiso para crear entrenamientos'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = EntrenamientoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)