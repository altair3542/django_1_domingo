# Helpdesk Pro

Sistema de helpdesk construido con Django para gestionar clientes, tickets, etiquetas y comentarios. El proyecto está pensado para correr en macOS y Windows sobre SQLite, sin necesidad de servicios externos.

## Qué incluye

- autenticación con login y logout
- página principal y layout base compartido
- listado de tickets con filtros por estado, prioridad y tag
- paginación del listado
- detalle de ticket con comentarios asociados
- creación y edición de tickets con formularios separados para usuarios normales y staff
- cierre de tickets mediante una acción dedicada por `POST`
- trazabilidad del cierre guardando un comentario interno

## Requisitos

- Python 3.10 o superior
- `pip`
- Git

La dependencia principal es Django, declarada en [`requirements.txt`](requirements.txt).

## Instalación

### macOS

```bash
git clone <URL_DEL_REPOSITORIO>
cd django_1_domingo
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
```

### Windows PowerShell

```powershell
git clone <URL_DEL_REPOSITORIO>
cd django_1_domingo
py -3 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
```

Si PowerShell bloquea la activación del entorno virtual, ejecuta una vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

## Cargar datos de prueba

El archivo [`seed_session3.py`](seed_session3.py) crea usuarios, clientes, tags, tickets y comentarios de ejemplo.

### macOS

```bash
python manage.py shell < seed_session3.py
```

### Windows PowerShell

```powershell
Get-Content seed_session3.py | python manage.py shell
```

El seed crea estos usuarios:

- `normal` / `12345678`
- `supervisor` / `12345678`

## Ejecutar el servidor

### macOS

```bash
python manage.py runserver
```

### Windows PowerShell

```powershell
python manage.py runserver
```

Luego abre `http://127.0.0.1:8000/`.

## Rutas principales

- `/` página de inicio
- `/login/` inicio de sesión
- `/logout/` cierre de sesión
- `/tickets/` listado de tickets
- `/tickets/new/` creación de ticket
- `/tickets/<id>/` detalle de ticket
- `/tickets/<id>/edit/` edición de ticket
- `/tickets/<id>/close/` cierre de ticket para staff
- `/admin/` panel administrativo de Django

## Comportamiento funcional

- el acceso a tickets requiere autenticación
- los usuarios normales pueden crear y editar tickets, pero no cerrarlos
- el staff puede cambiar estados operativos desde la edición, pero no cerrar desde ese formulario
- el cierre real se hace desde la acción dedicada y agrega un comentario interno para dejar evidencia
- el listado usa select relacionados y conteo de comentarios para evitar consultas innecesarias

## Estructura del proyecto

- [`config/`](config/) configuración principal de Django
- [`core/`](core/) página home y vistas generales
- [`helpdesk/`](helpdesk/) dominio del helpdesk, formularios, vistas, modelos y tests
- [`static/`](static/) archivos estáticos
- [`db.sqlite3`](db.sqlite3) base de datos local por defecto

## Ejecutar pruebas

```bash
python manage.py test
```

## Notas útiles

- La base de datos por defecto es SQLite y vive en [`db.sqlite3`](db.sqlite3).
- El login redirige al listado de tickets.
- Si quieres volver a una base limpia con datos de ejemplo, vuelve a ejecutar las migraciones y el seed.

## Flujo rápido

1. Crear y activar el entorno virtual.
2. Instalar dependencias con `pip install -r requirements.txt`.
3. Ejecutar `python manage.py migrate`.
4. Cargar datos con `seed_session3.py`.
5. Iniciar el servidor con `python manage.py runserver`.
6. Entrar a `/login/` con `normal` o `supervisor`.
