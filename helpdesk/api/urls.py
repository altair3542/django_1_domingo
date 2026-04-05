from django.urls import path

from .views import TicketApiListView

app_name = "api"

urlpatterns = [
    path("tickets/", TicketApiListView.as_view(), name="ticket_list"),
]
