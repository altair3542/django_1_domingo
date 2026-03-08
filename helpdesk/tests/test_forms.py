from django.test import TestCase
from helpdesk.forms import TicketForm
from helpdesk.models import Ticket
from .factories import make_customer

class TicketFormTest(TestCase):
    def Test_title_min_length(self):
        c = make_customer()
        form = TicketForm(data={
            "title": "corto",
            "customer": c.id,
            "status": Ticket.Status.OPEN,
            "priority" : Ticket.Priority.MEDIUM
        })
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

        
