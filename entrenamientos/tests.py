from rest_framework.test import APITestCase
from django.contrib.auth.models import User, Group
from perros.models import Perro
from .models import Entrenamiento
from rest_framework import status
class EntrenamientoAPITest(APITestCase):

    def setUp(self):
        self.admin_group = Group.objects.create(name='Administradores')
        self.guia_group = Group.objects.create(name='Guias')
        self.entrenador_group = Group.objects.create(name='Entrenadores')

        self.admin = User.objects.create_user(
            username='admin_api', password='admin123'
        )
        self.admin.groups.add(self.admin_group)

        self.guia = User.objects.create_user(
            username='guia_api', password='guia123'
        )
        self.entrenador = User.objects.create_user(
            username='entrenador_test',
            password='12345'
        )
        self.entrenador.groups.add(self.entrenador_group)

        self.guia.groups.add(self.guia_group)

        self.perro = Perro.objects.create(
            nombre='Rocky',
            raza='Pastor',
            edad=4,
            propietario=self.guia
        )

        self.entrenamiento = Entrenamiento.objects.create(
            perro=self.perro,
            tipo='Nivel 1',
            fecha='2026-01-01',
            duracion=60
        )
    def test_admin_puede_ver_entrenamientos(self):
        self.client.login(username='admin_api', password='admin123')
        response = self.client.get('/api/entrenamientos-func/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
    def test_guia_ve_solo_sus_entrenamientos(self):
        self.client.login(username='guia_api', password='guia123')
        response = self.client.get('/api/entrenamientos-func/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
    def test_guia_no_puede_crear_entrenamiento(self):
        self.client.login(username='guia_api', password='guia123')
        data = {
            'perro': self.perro.id,
            'tipo': 'Nivel 2',
            'fecha': '2026-02-01',
            'duracion': 90
        }
        response = self.client.post('/api/entrenamientos-func/', data)
        self.assertEqual(response.status_code, 403)
    def test_usuario_sin_grupo_no_ve_datos(self):
        user = User.objects.create_user(
            username='sin_grupo',
            password='12345'
        )

        self.client.login(username='sin_grupo', password='12345')

        response = self.client.get('/api/entrenamientos-func/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
    def test_entrenador_puede_crear_entrenamiento(self):
        self.client.login(
            username='entrenador_test',
            password='12345'
        )

        data = {
            'perro': self.perro.id,
            'tipo': 'Nivel 2',
            'fecha': '2026-02-01',
            'duracion': 90
        }

        response = self.client.post(
            '/api/entrenamientos-func/',
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Entrenamiento.objects.count(), 2)


