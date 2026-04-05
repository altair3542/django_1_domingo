from django.test import TestCase
from django.urls import reverse

from helpdesk.models import Ticket

from .factories import make_customer, make_ticket, make_user


class TicketListAuthTest(TestCase):
    def test_ticket_list_require_login(self):
        response = self.client.get(reverse("ticket_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response["Location"])

    def test_ticket_list_ok_when_logged_in(self):
        user = make_user()
        self.client.login(username=user.username, password="pass12345")
        response = self.client.get(reverse("ticket_list"))
        self.assertEqual(response.status_code, 200)


class TicketUpdateAuthzTest(TestCase):
    def setUp(self):
        self.customer = make_customer()
        self.ticket = make_ticket(self.customer)

    def test_normal_user_cannot_close_via_generic_update(self):
        user = make_user(username="normal", is_staff=False)
        self.client.login(username=user.username, password="pass12345")
        response = self.client.post(
            reverse("ticket_update", kwargs={"pk": self.ticket.pk}),
            data={
                "title": "Ticket suficientemente largo",
                "customer": self.customer.id,
                "priority": Ticket.Priority.HIGH,
                "status": Ticket.Status.CLOSED,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.ticket.refresh_from_db()
        self.assertNotEqual(self.ticket.status, Ticket.Status.CLOSED)

    def test_staff_user_cannot_close_via_generic_update(self):
        user = make_user(username="staff", is_staff=True)
        self.client.login(username=user.username, password="pass12345")
        response = self.client.post(
            reverse("ticket_update", kwargs={"pk": self.ticket.pk}),
            data={
                "title": "Ticket suficientemente largo",
                "customer": self.customer.id,
                "priority": Ticket.Priority.HIGH,
                "status": Ticket.Status.CLOSED,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.ticket.refresh_from_db()
        self.assertNotEqual(self.ticket.status, Ticket.Status.CLOSED)
