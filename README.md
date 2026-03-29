# Django Helpdesk — Sesión 2

Proyecto Django con módulo de Helpdesk orientado a:

- Modelado relacional (`Customer`, `Ticket`, `Tag`, `Comment`)
- Listado y detalle de tickets con Class-Based Views
- Filtros por estado, prioridad y tag
- Paginación y conteo de comentarios por ticket

## Requisitos

- Python 3.10+
- pip
- SQLite (incluido con Python)

Dependencia principal en `requirements.txt`:

- `Django>=5.0,<6.0`

## Estructura (resumen)

- `config/`: configuración del proyecto (`settings.py`, `urls.py`)
- `helpdesk/`: app principal (modelos, vistas, rutas, templates, tests)
- `seed_session2.py`: script para cargar datos de ejemplo
- `db.sqlite3`: base local para desarrollo

## Instalación y arranque

1. Crear entorno virtual

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Aplicar migraciones

```bash
python manage.py migrate
```

4. (Opcional) Cargar datos de sesión 2

```bash
python manage.py shell < seed_session2.py
```

5. Ejecutar servidor

```bash
python manage.py runserver
```

## Rutas disponibles

- `GET /tickets/` -> listado de tickets (nombre: `helpdesk:ticket_list`)
- `GET /tickets/<id>/` -> detalle de ticket (nombre: `helpdesk:ticket_detail`)

La URL raíz del proyecto (`/`) está conectada a `helpdesk.urls`.

## Uso de filtros y paginación

En el listado puedes combinar query params:

- `status`: `open`, `in_progress`, `closed`
- `priority`: `1`, `2`, `3`
- `tag`: slug del tag
- `page`: número de página

Ejemplos:

```text
/tickets/?status=open
/tickets/?priority=3&tag=urgent
/tickets/?status=in_progress&page=2
```

## Notas técnicas

- `TicketListView` usa métodos del manager/queryset:
	- `with_related()`
	- `with_comment_count()`
	- `ordered()`
- El detalle (`TicketDetailView`) precarga relaciones para evitar consultas extra.
- El proyecto define `STATICFILES_DIRS = [BASE_DIR / "static"]`.
	Si no existe la carpeta `static/`, Django muestra un warning (`staticfiles.W004`) al correr checks/tests.

## Ejecutar pruebas

```bash
python manage.py test helpdesk.tests
```

Estado actual del repositorio:

- Existen pruebas heredadas de una versión con autenticación/cierre de tickets (`ticket_close`, `reverse("ticket_list")`) que no coinciden con las rutas actuales namespaced.
- Por esa razón, al ejecutar toda la suite de `helpdesk.tests` hoy aparecen errores de `NoReverseMatch`.

## Comandos útiles

```bash
python manage.py check
python manage.py showmigrations
python manage.py makemigrations
python manage.py migrate
```

## Licencia

Uso académico / educativo.
