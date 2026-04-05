from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import TicketForm, TicketStaffForm
from .models import Comment, Tag, Ticket


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        messages.error(self.request, "No tienes permisos para realizar esta acción.")
        return redirect("ticket_list")


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "helpdesk/ticket_list.html"
    context_object_name = "tickets"
    paginate_by = 10

    def get_queryset(self):
        status = self.request.GET.get("status") or None
        priority = self.request.GET.get("priority") or None
        tag = self.request.GET.get("tag") or None

        return (
            Ticket.objects.with_related_for_listing()
            .with_comment_count()
            .filter_by_params(status=status, priority=priority, tag=tag)
            .ordered_for_listing()
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_status = self.request.GET.get("status", "")
        current_priority = self.request.GET.get("priority", "")
        current_tag = self.request.GET.get("tag", "")

        params = self.request.GET.copy()
        params.pop("page", None)

        context.update(
            {
                "status_choices": Ticket.Status.choices,
                "priority_choices": Ticket.Priority.choices,
                "available_tags": Tag.objects.all(),
                "current_status": current_status,
                "current_priority": current_priority,
                "current_tag": current_tag,
                "page_querystring": urlencode(params, doseq=True),
            }
        )
        return context


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    template_name = "helpdesk/ticket_form.html"
    success_url = reverse_lazy("ticket_list")

    def get_form_class(self):
        if self.request.user.is_staff:
            return TicketStaffForm
        return TicketForm

    def form_valid(self, form):
        messages.success(self.request, "Ticket creado correctamente.")
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    template_name = "helpdesk/ticket_form.html"

    def get_form_class(self):
        if self.request.user.is_staff:
            return TicketStaffForm
        return TicketForm

    def form_valid(self, form):
        messages.success(self.request, "Ticket actualizado correctamente.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("ticket_detail", kwargs={"pk": self.object.pk})


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "helpdesk/ticket_detail.html"
    context_object_name = "ticket"

    def get_queryset(self):
        return Ticket.objects.select_related("customer").prefetch_related("tags", "comments")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_close_ticket"] = (
            self.request.user.is_staff and self.object.status != Ticket.Status.CLOSED
        )
        return context


class TicketCloseView(StaffRequiredMixin, View):
    """
    Acción sensible del dominio: cerrar ticket solo por POST y solo para staff.
    Además deja evidencia en Comment para trazabilidad operativa.
    """

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, pk=pk)

        if ticket.status == Ticket.Status.CLOSED:
            messages.info(request, "El ticket ya estaba cerrado.")
            return redirect("ticket_detail", pk=ticket.pk)

        ticket.status = Ticket.Status.CLOSED
        ticket.save(update_fields=["status"])

        Comment.objects.create(
            ticket=ticket,
            author_name=request.user.get_username() or "staff",
            body="Ticket cerrado por staff desde la acción dedicada de cierre.",
            is_internal=True,
        )

        messages.success(request, "Ticket cerrado correctamente.")
        return redirect("ticket_detail", pk=ticket.pk)

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(["POST"])
