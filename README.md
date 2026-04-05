# Helpdesk Pro - Estado hasta sesión 3

Proyecto Django intermedio/avanzado para el curso. Este estado incluye:

- sesión 1: dominio enriquecido con `Tag` y `Comment`
- sesión 2: listados con filtros, paginación y conteo de comentarios
- sesión 3: permisos por rol, formularios robustos y cierre de tickets por acción dedicada

## Requisitos

```bash
pip install -r requirements.txt
```

## Migraciones

```bash
python manage.py migrate
```

## Seed de sesión 3

Carga datos de prueba y dos usuarios:

- normal / 12345678
- supervisor / 12345678

Ejecución:

```bash
python manage.py shell < seed_session3.py
```

## Servidor

```bash
python manage.py runserver
```

## Flujo esperado de la sesión 3

- usuarios normales pueden crear y editar tickets, pero no cerrarlos
- staff puede cerrar tickets solo desde la acción dedicada
- el cierre se hace por `POST`, con `CSRF` y deja evidencia en `Comment`
