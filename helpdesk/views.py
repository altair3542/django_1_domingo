from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from .forms import TicketForm
from .models import Ticket

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "helpdesk/ticket_list.html"
    context_object_name = "tickets"
    paginate_by = 20

    def get_queryset(self):
        qs = Ticket.objects.select_related("customer").order_by("-created_at")
        status = self.request.GET.get("status")
        if status:
            qs = qs.filter(status=status)
        return qs


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = "helpdesk/ticket_form.html"
    success_url = reverse_lazy("ticket_list")

    def form_valid(self, form):
        messages.success(self.request, "Ticket creado correctamente.")
        return super().form_valid(form)


class TicketUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = "helpdesk/ticket_form.html"

    def get_success_url(self):
        messages.success(self.request, "Ticket actualizado.")
        return reverse_lazy("ticket_detail", kwargs={"pk": self.object.pk})


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = "helpdesk/ticket_detail.html"
    context_object_name = "ticket"


def is_staff(user):
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def close_ticket(request, pk: int):
    if request.method != "POST":
        return HttpResponseForbidden("Método no permitido")

    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.status = Ticket.Status.CLOSED
    ticket.save(update_fields=["status"])
    messages.success(request, "Ticket cerrado.")
    return redirect("ticket_detail", pk=ticket.pk)
