from django.test import TestCase
from django.urls import reverse
from helpdesk.models import Ticket
from .factories import make_user, make_customer, make_ticket

class CloseTicketTest(TestCase):
    def setUp(self):
        self.customer = make_customer()
        self.ticket = make_ticket(self.customer)

    def test_close_requires_staff(self):
        user = make_user(username="u1", is_staff=False)
        self.client.login(username= "u1", password="pass12345")
        resp = self.client.get(reverse("ticket_close", kwargs={"pk": self.ticket.pk}))
        self.assertIn(resp.status_code, (302, 403))

    def test_close_requires_post(self):
        staff = make_user(username="staff", is_staff=True)
        self.client.login(username="staff", password="pass12345")
        resp = self.client.get(reverse("ticket_close", kwargs={"pk": self.ticket.pk}))
        self.assertEqual(resp.status_code, 403)

    def test_close_sets_status_closed(self):
        staff = make_user(username = "staff2", is_staff=True)
        self.client.login(username = "staff2", password = "pass12345")
        resp = self.client.post(reverse("ticket_close", kwargs={"pk": self.ticket.pk}))
        self.assertIn(resp.status_code,(302, 200))
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.CLOSED)
