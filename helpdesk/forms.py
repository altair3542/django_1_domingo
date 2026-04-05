from django import forms

from .models import Customer, Ticket


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email"]

    def clean_email(self):
        return self.cleaned_data["email"].strip().lower()


class BaseTicketForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 8:
            raise forms.ValidationError("El título debe tener al menos 8 caracteres.")
        return title


class TicketForm(BaseTicketForm):
    """
    Formulario para usuario normal.
    No expone el estado porque cerrar tickets no hace parte de su capacidad.
    """

    class Meta:
        model = Ticket
        fields = ["title", "customer", "priority", "tags"]


class TicketStaffForm(BaseTicketForm):
    """
    Formulario para staff.
    Puede mover estados operativos, pero no cerrar tickets desde la edición genérica.
    El cierre debe pasar por la acción dedicada.
    """

    class Meta:
        model = Ticket
        fields = ["title", "customer", "status", "priority", "tags"]

    def clean_status(self):
        status = self.cleaned_data["status"]
        if status == Ticket.Status.CLOSED:
            raise forms.ValidationError(
                "El cierre del ticket debe hacerse desde la acción dedicada de cierre."
            )
        return status
