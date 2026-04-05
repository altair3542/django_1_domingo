from django.test import TestCase
from django.urls import reverse

from helpdesk.models import Comment, Ticket

from .factories import make_customer, make_ticket, make_user


class CloseTicketTest(TestCase):
    def setUp(self):
        self.customer = make_customer()
        self.ticket = make_ticket(self.customer)

    def test_close_requires_staff(self):
        make_user(username="u1", is_staff=False)
        self.client.login(username="u1", password="pass12345")
        response = self.client.post(reverse("ticket_close", kwargs={"pk": self.ticket.pk}))
        self.assertEqual(response.status_code, 302)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.OPEN)

    def test_close_requires_post(self):
        make_user(username="staff", is_staff=True)
        self.client.login(username="staff", password="pass12345")
        response = self.client.get(reverse("ticket_close", kwargs={"pk": self.ticket.pk}))
        self.assertEqual(response.status_code, 405)

    def test_close_sets_status_closed_and_creates_audit_comment(self):
        make_user(username="staff2", is_staff=True)
        self.client.login(username="staff2", password="pass12345")
        response = self.client.post(reverse("ticket_close", kwargs={"pk": self.ticket.pk}))
        self.assertEqual(response.status_code, 302)
        self.ticket.refresh_from_db()
        self.assertEqual(self.ticket.status, Ticket.Status.CLOSED)
        self.assertTrue(
            Comment.objects.filter(
                ticket=self.ticket,
                author_name="staff2",
                is_internal=True,
            ).exists()
        )
