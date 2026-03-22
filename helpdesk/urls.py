# helpdesk/urls.py
# from django.urls import path
# from . import views

# urlpatterns = [
#     path("tickets/", views.TicketListView.as_view(), name="ticket_list"),
#     path("tickets/new/", views.TicketCreateView.as_view(), name="ticket_create"),
#     path("tickets/<int:pk>/", views.TicketDetailView.as_view(), name="ticket_detail"),
#     path("tickets/<int:pk>/edit/", views.TicketUpdateView.as_view(), name="ticket_update"),
#     path("tickets/<int:pk>/close/", views.close_ticket, name="ticket_close"),
# ]

from django.urls import path
from .views import TicketDetailView, TicketListView

app_name = "helpdesk"

urlpatterns = [
    path("tickets/", TicketListView.as_view(), name="ticket_list"),
    path("tickets/<int:pk>/", TicketDetailView.as_view(), name="ticket_detail"),
]

