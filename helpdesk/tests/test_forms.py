from django.test import TestCase

from helpdesk.forms import TicketForm, TicketStaffForm
from helpdesk.models import Ticket

from .factories import make_customer


class TicketFormTest(TestCase):
    def test_title_min_length_for_normal_user(self):
        customer = make_customer()
        form = TicketForm(
            data={
                "title": "corto",
                "customer": customer.id,
                "priority": Ticket.Priority.MEDIUM,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_staff_form_rejects_closed_status_in_generic_edit(self):
        customer = make_customer()
        form = TicketStaffForm(
            data={
                "title": "Ticket suficientemente largo",
                "customer": customer.id,
                "status": Ticket.Status.CLOSED,
                "priority": Ticket.Priority.MEDIUM,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("status", form.errors)
