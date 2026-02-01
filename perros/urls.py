from django.urls import path
from .views import *


urlpatterns = [
    path('perros/', PerroListView.as_view(), name='perro-list'),
    path('perros/<int:pk>/', PerroDetailView.as_view(), name='perro-detail'),
    path('perros/crear/', PerroCreateView.as_view(), name='perro-create'),
    path('perros/<int:pk>/editar/', PerroUpdateView.as_view(), name='perro-update'),
    path('perros/<int:pk>/eliminar/', PerroDeleteView.as_view(), name='perro-delete'),
]

