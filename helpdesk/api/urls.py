from django.urls import path

from .views import (
    ApiCsrfView,
    ApiLoginView,
    ApiLogoutView,
    TicketApiListView,
)

app_name = "api"

urlpatterns = [
    path("auth/csrf/", ApiCsrfView.as_view(), name="auth_csrf"),
    path("auth/login/", ApiLoginView.as_view(), name="auth_login"),
    path("auth/logout/", ApiLogoutView.as_view(), name="auth_logout"),
    path("tickets/", TicketApiListView.as_view(), name="ticket_list"),
]
