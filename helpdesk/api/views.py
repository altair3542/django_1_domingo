from django.db.models import Count
from django.http import JsonResponse
from django.views import View

from helpdesk.models import Ticket

class TicketApiListView(View):
    # Mini api de lectura para tickets, devuevle json y requiere autenticacion

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {"detail": "identificate, identificate en esta mondá."},
                status=401
            )
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        queryset = (
            Tickets.objects.select_related("customer")
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
            queryset = queryset.filter(tag=tag)

        queryset = queryset.distinct

        if limit:
            try:
                limit_value = int(limit)
            except ValueError:
                return JsonResponse(
                    {"detail" : "Limite de parametro invalido."},
                    status=400
                )

            if limit_value <= 0:
                return JsonResponse(
                    return JsonResponse(
                        {"detail": "El limite debe ser mayor a cero"}
                    )
                )

            query = queyset[:limit_value]

        results = [self.serialize_ticket(ticket) for ticket in queryset]

        return JsonResponse(
            {
                "count" : len(results),
                "results": results
            }
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
