from django.shortcuts import render
from .models import Ticket
# Create your views here.
def ticket_list(request):
    tickets = Ticket.objects.select_related("customer").order_by("-created_at")
    return render(request, "helpdesk/ticket_list.html", {"title": "Tickets", "tickets": tickets})
