from django.contrib import admin
from .models import Customer, Ticket
# Register your models here.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "customer", "status", "priority", "created_at")
    search_fields = ("title", "customer__name", "customer__email")
    list_filter = ("status", "priority")
    list_select_related = ("customer",)

admin.site.register(Customer)
