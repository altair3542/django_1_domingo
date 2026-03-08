from django.test import TestCase
from django.urls import reverse
from .factories import make_user


class TicketListAuthTest(TestCase):
    def test_ticket_list_require_login(self):
        resp = self.client.get(reverse("ticket_list"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/", resp["Location"])

    def test_ticket_list_ok_when_logged_in(self):
        user = make_user()
        self.client.login(username=user.username, password="pass12345")
        resp = self.client.get(reverse("ticket_list"))
        self.assertEqual(resp.status_code, 200)
