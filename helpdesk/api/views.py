import json

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator
from django.db.models import Count

from helpdesk.models import Ticket


@method_decorator(ensure_csrf_cookie, name="dispatch")
class ApiCsrfView(View):
    """
    Fuerza la emisión de la cookie csrftoken.
    Útil para frontends separados que usan sesión + CSRF.
    """

    def get(self, request, *args, **kwargs):
        return JsonResponse({"detail": "CSRF cookie set."}, status=200)


@method_decorator(csrf_protect, name="dispatch")
class ApiLoginView(View):
    """
    Login JSON basado en sesión de Django.
    Requiere CSRF válido.
    """

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse(
                {"detail": "Invalid JSON payload."},
                status=400,
            )

        username = (data.get("username") or "").strip()
        password = data.get("password") or ""

        if not username or not password:
            return JsonResponse(
                {"detail": "Username and password are required."},
                status=400,
            )

        user = authenticate(request, username=username, password=password)

        if user is None:
            return JsonResponse(
                {"detail": "Invalid credentials."},
                status=401,
            )

        login(request, user)

        return JsonResponse(
            {
                "detail": "Login successful.",
                "user": {
                    "id": user.id,
                    "username": user.get_username(),
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                },
            },
            status=200,
        )


@method_decorator(csrf_protect, name="dispatch")
class ApiLogoutView(View):
    """
    Logout JSON basado en sesión.
    Requiere CSRF válido.
    """

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {"detail": "You are not logged in."},
                status=401,
            )

        logout(request)

        return JsonResponse(
            {"detail": "Logout successful."},
            status=200,
        )


class TicketApiListView(View):
    """
    Mini API de lectura para tickets.
    Requiere autenticación y devuelve JSON.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {"detail": "Authentication credentials were not provided."},
                status=401,
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        queryset = (
            Ticket.objects.select_related("customer")
            .prefetch_related("tags")
            .annotate(comment_count=Count("comments", distinct=True))
            .order_by("-created_at", "-id")
        )

        status = request.GET.get("status")
        priority = request.GET.get("priority")
        tag = request.GET.get("tag")
        limit = request.GET.get("limit")

        if status:
            queryset = queryset.filter(status=status)

        if priority:
            queryset = queryset.filter(priority=priority)

        if tag:
            queryset = queryset.filter(tags__slug=tag)

        queryset = queryset.distinct()

        if limit:
            try:
                limit_value = int(limit)
            except ValueError:
                return JsonResponse(
                    {"detail": "Invalid limit parameter."},
                    status=400,
                )

            if limit_value <= 0:
                return JsonResponse(
                    {"detail": "Limit must be greater than 0."},
                    status=400,
                )

            queryset = queryset[:limit_value]

        results = [self.serialize_ticket(ticket) for ticket in queryset]

        return JsonResponse(
            {
                "count": len(results),
                "results": results,
            },
            status=200,
        )

    def serialize_ticket(self, ticket):
        return {
            "id": ticket.id,
            "title": ticket.title,
            "status": ticket.status,
            "status_label": ticket.get_status_display(),
            "priority": ticket.priority,
            "priority_label": ticket.get_priority_display(),
            "customer": {
                "id": ticket.customer_id,
                "name": ticket.customer.name,
                "email": ticket.customer.email,
            },
            "tags": [
                {
                    "id": tag.id,
                    "name": tag.name,
                    "slug": tag.slug,
                }
                for tag in ticket.tags.all()
            ],
            "comment_count": ticket.comment_count,
            "created_at": ticket.created_at.isoformat(),
        }
