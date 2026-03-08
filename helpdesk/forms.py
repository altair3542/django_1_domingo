from django import forms
from .models import Customer, Ticket

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email"]

    def clean_email(self):
        # Evita duplicados por mayusculas y espacios.
        return self.cleaned_data["email"].strip().lower()

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "customer", "priority"]

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 8:
            raise forms.ValidationError("El título debe tener al menos 8 caracteres.")
        return title

class TicketStaffForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "customer", "status", "priority"]

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 8:
            raise forms.ValidationError("El título debe tener al menos 8 caracteres.")
        return title
