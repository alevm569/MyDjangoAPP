from django.urls import include, path
from .views import *
from rest_framework.routers import DefaultRouter
from entrenamientos.views import EntrenamientoDeleteView
from .views import entrenamientos_api

router = DefaultRouter()
router.register(r'api/entrenamientos', EntrenamientoViewSet, basename='entrenamiento')


urlpatterns = [
    path('entrenamientos/', EntrenamientoListView.as_view(), name='entrenamiento-list'),
    path('entrenamientos/<int:pk>/', EntrenamientoDetailView.as_view(), name='entrenamiento-detail'),
    path('entrenamientos/crear/', EntrenamientoCreateView.as_view(), name='entrenamiento-create'),
    path('entrenamientos/<int:pk>/editar/', EntrenamientoUpdateView.as_view(), name='entrenamiento-update'),
    path('entrenamientos/<int:pk>/eliminar/', EntrenamientoDeleteView.as_view(), name='entrenamiento-delete'),

    path('api/entrenamientos-func/', entrenamientos_api),
    path('api/', include(router.urls)),
]
