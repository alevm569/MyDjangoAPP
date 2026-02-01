# MyDjangoAPP – Sistema de Adiestramiento de Perros
Este proyecto corresponde al desarrollo de un backend en Django que implementa un sistema de gestión de adiestramiento de perros, utilizando Django REST Framework (DRF) para exponer una API REST y controlando el acceso mediante roles de usuario.

El sistema permite registrar perros, gestionar sus entrenamientos y restringir el acceso a la información según el rol del usuario autenticado.

El proyecto se basa en un escenario realista de adiestramiento canino, donde intervienen distintos tipos de usuarios:

Administradores: gestionan completamente el sistema.

- Entrenadores: registran y consultan entrenamientos.

- Guías (propietarios): solo pueden visualizar la información relacionada con sus propios perros.

- Este enfoque permite aplicar control de acceso y autorización basada en roles.

## Estructura del Proyecto

```
MyDjangoAPP/
│
├── adiestramiento_backend/   # Proyecto principal
├── perros/                  # App para gestión de perros
├── entrenamientos/           # App para gestión de entrenamientos
└── manage.py
│── requirements.txt
│── .env

```
## Instalación de Dependencias

```
pip install -r requirements.txt
```

## Base de datos
Modelos implementados
#### Perro 
- nombre
- raza
- edad
- propietario (ForeignKey a User)
- fecha_registro

#### Entrenamiento
- perro (ForeignKey a Perro)
- tipo
- fecha
- duracion
- observaciones

### Usuarios y Grupos
Para validar el funcionamiento del sistema se crearon los siguientes usuarios:
´´´
admin1       | adiestra360
entrenador1  | adiestra360e
guia1        | adiestra360g

´´´
## Vistas Web
Se implementaron vistas genéricas basadas en clases (CBV) para los modelos Perro y Entrenamiento, utilizando:
- ListView
- DetailView
- CreateView
- UpdateView
- DeleteView

El acceso está protegido mediante:
- LoginRequiredMixin
- UserPassesTestMixin
- Validación de grupos (Administradores, Entrenadores, Guias)

Las vistas web están implementadas a nivel de lógica, sin embargo:
- Solo se desarrolló el template HTML para el listado de perros.
- Las vistas de entrenamientos no cuentan con templates HTML.

## API REST
Se configuró Django REST Framework utilizando autenticación por sesión.
### ViewSet
Se implementó un ModelViewSet para el modelo Entrenamiento, permitiendo:
- Listar entrenamientos
- Crear entrenamientos
- Editar entrenamientos
- Eliminar entrenamientos

El acceso a los datos está controlado según el rol del usuario:
- Administradores: acceso total
- Entrenadores: acceso total
Guías: solo pueden ver entrenamientos de sus propios perros

Permisos
Las operaciones de escritura están restringidas mediante lógica basada en grupos de usuarios, validada directamente en las vistas y durante las pruebas funcionales.

### API VIEW
Se implementa un endpoint adicional utilizando @api_view, demostrando el manejo manual de métodos HTTP (GET, POST) y control de permisos.

Endpoint funcional:
´´´
/api/entrenamientos-func/

´´´
### Autenticación
La autenticación se maneja mediante sesiones, utilizando Django REST Framework.
Login para la API:
´´´
/api-auth/login/

´´´

### Permisos y control de acceso
Aunque Django proporciona permisos automáticos (add, change, delete, view), el proyecto utiliza principalmente control de acceso basado en grupos, evaluado directamente en las vistas y endpoints de la API.

## Ejecución del proyecto
Instalar dependencias:
```
pip install -r requirements.txt
```

Aplicar migraciones:
```
python manage.py migrate
```

Ejecutar servidor:
```
python manage.py runserver
```

## Conclusiones y Observaciones
- Aunque la respuesta HTTP indica los métodos permitidos por el endpoint, las operaciones de creación y modificación están restringidas mediante lógica de permisos basada en grupos de usuario, validada durante las pruebas funcionales.
- Es importante destacar que la sesión del admin de Django es distinta a la sesión utilizada por la API REST.
- El enfoque utilizado para los permisos y control de acceso, permite una mayor flexibilidad y claridad en la lógica de autorización.

## URL: 
https://github.com/alevm569/MyDjangoAPP
