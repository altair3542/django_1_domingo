# Django 1 — Sesión 1 (MVT, rutas, vistas y plantillas)

Proyecto base en Django para la Sesión 1 del temario: **ruteo**, **vistas (FBV)**, **templates con herencia** y **archivos estáticos**.

---

## Requisitos
- Python **3.9+** (recomendado 3.11/3.12)
- `pip`
- macOS / Linux / Windows

> **Nota (macOS):** normalmente usarás `python3` y `pip3`.

---

## Estructura (resumen)
- `config/`: settings y urls raíz del proyecto
- `core/`: app principal (views y urls)
- `templates/`: templates globales (`base.html`) y de la app (`core/`)
- `static/`: archivos estáticos (CSS)

---

## Instalación inicial

### 1) Crear y activar entorno virtual
**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2) Instalar dependencias
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Ejecutar el servidor
```bash
python manage.py runserver
```

Abrir:
- Home: http://127.0.0.1:8000/
- Catálogo: http://127.0.0.1:8000/catalog/

---

## Rutinas de trabajo “día a día” (lo que harás siempre)

### Opción A: cada día (normal)
1) Ir a la carpeta del proyecto  
2) Activar venv  
3) Levantar servidor

**macOS / Linux**
```bash
cd /ruta/al/proyecto
source .venv/bin/activate
python manage.py runserver
```

**Windows (PowerShell)**
```powershell
cd C:\ruta\al\proyecto
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

---

## Equipos con DeepFreeze / restauración al apagar (estado “se pierde”)

En laboratorios o PCs con DeepFreeze, todo lo que guardes en el disco “congelado” puede revertirse al reiniciar.
Esto afecta especialmente:
- `.venv/` (entorno virtual)
- instalaciones locales de paquetes
- caches temporales

### Recomendación 1 (ideal): guardar el proyecto en una zona NO congelada
- Disco/partición “D:” (en Windows) si existe.
- Carpeta de red, USB, o una ruta explícitamente persistente.
- En macOS: depende de la política del laboratorio; si el usuario tiene carpeta persistente, úsala.

Así mantienes el repo y (si está permitido) incluso `.venv/`.

### Recomendación 2 (realista): recrear el venv **rápido** cada sesión
Si TODO se borra al apagar, asume que **cada día** debes recrear `.venv/` e instalar dependencias desde `requirements.txt`.

**macOS / Linux**
```bash
cd /ruta/al/proyecto
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python manage.py runserver
```

**Windows (PowerShell)**
```powershell
cd C:\ruta\al\proyecto
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python manage.py runserver
```

### Recomendación 3: tener una “carpeta de backup” y restaurar
Si el proyecto también se pierde:
- Mantén un `.zip` del proyecto en USB/Drive.
- Lo descomprimes al inicio de la clase y ejecutas el bloque de comandos anterior.

---

## Rutas disponibles
- `/` → `core.views.home` (name: `home`)
- `/catalog/` → `core.views.catalog` (name: `catalog`)

---

## Templates
- `templates/base.html`: layout base + carga CSS con `{% load static %}`
- `templates/core/home.html`: hereda de `base.html`
- `templates/core/catalog.html`: hereda de `base.html`

---

## Static files
- CSS: `static/css/app.css`
- Config: `STATICFILES_DIRS = [BASE_DIR / "static"]`

---

## Troubleshooting

### NameError en URLs (ej: `name=catalog`)
En `core/urls.py`, el parámetro `name` debe ser string:
```python
path("catalog/", views.catalog, name="catalog")
```

### TemplateDoesNotExist
Verifica:
- existe `templates/base.html` y `templates/core/*.html`
- en `settings.py`: `TEMPLATES[0]["DIRS"]` incluye `BASE_DIR / "templates"`

### CSS no carga
Verifica:
- `{% load static %}` en `base.html`
- `<link rel="stylesheet" href="{% static 'css/app.css' %}">`
- `STATICFILES_DIRS` configurado
- DevTools → Network → `/static/css/app.css` devuelve 200

---

## Git
Este repo ignora:
- `.venv/` (entorno virtual)
- `__pycache__/` (cache de Python)
- `.DS_Store`, `.vscode/`, `.idea/`, etc.

---

## Licencia
Uso académico / educativo.
