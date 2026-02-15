from django.shortcuts import render

# Create your views here.
def home(request):
    context = {
        "title": "Home",
        "message": "Hola Django: Request -> View -> Template -> Response",
    }
    return render(request, "core/home.html", context)

def catalog(request):
    context = {
        "title": "Catalogo",
        "items": [
            {"name": "Elemento A", "tag": "demo"},
            {"name": "Elemento B", "tag": "demo"},
            {"name": "Elemento C", "tag": "demo"},
        ],
    }
    return render(request, "core/catalog.html", context)
