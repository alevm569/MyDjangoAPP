from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Perro

class PerroListView(LoginRequiredMixin, ListView):
    model = Perro
    template_name = 'perros/perro_list.html'
    context_object_name = 'perros'

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='Administradores').exists():
            return Perro.objects.all()

        if user.groups.filter(name='Entrenadores').exists():
            return Perro.objects.all()

        if user.groups.filter(name='Guias').exists():
            return Perro.objects.filter(propietario=user)

        return Perro.objects.none()
    
class PerroDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Perro
    template_name = 'perros/perro_detail.html'

    def get_queryset(self):
        user = self.request.user

        if user.groups.filter(name='Guias').exists():
            return Perro.objects.filter(propietario=user)

        return Perro.objects.all()
    
class PerroCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Perro
    fields = ['nombre', 'raza', 'edad', 'propietario']
    success_url = reverse_lazy('perro-list')

    def test_func(self):
        return self.request.user.groups.filter(name='Administradores').exists()
    
class PerroUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Perro
    fields = ['nombre', 'raza', 'edad', 'propietario']
    success_url = reverse_lazy('perro-list')

    def test_func(self):
        return self.request.user.groups.filter(name='Administradores').exists()
    
class PerroDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Perro
    success_url = reverse_lazy('perro-list')

    def test_func(self):
        return self.request.user.groups.filter(name='Administradores').exists()
    
