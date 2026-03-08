from django.contrib.auth import get_user_model
from helpdesk.models import Customer, Ticket

User = get_user_model()

def make_user(username="user", password="pass12345", is_staff=False):
    return User.objects.create_user(
        username=username,
        password=password,
        is_staff=is_staff
    )

def make_customer(name="Acme", email="soporte@acme.com"):
    return Customer.objects.create(name=name, email=email)

def make_ticket(customer, title="no puedo iniciar sesion", status=Ticket.Status.OPEN, priority=Ticket.Priority.MEDIUM):
    return Ticket.objects.create(
        title=title,
        customer=customer,
        status=status,
        priority=priority
    )
