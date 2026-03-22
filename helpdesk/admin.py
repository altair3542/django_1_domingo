from django.contrib import admin
from .models import Comment, Customer, Tag, Ticket
# Register your models here.
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "created_at")
    search_fields = ("name", "email", "company")
    ordering = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ("author_name", "is_internal", "body", "created_at")
    readonly_fields = ("created_at",)
    show_change_link = True


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "customer",
        "status",
        "priority",
        "created_at",
    )
    list_filter = ("status", "priority", "tags")
    search_fields = ("title", "customer__name", "customer__email")
    autocomplete_fields = ("customer",)
    list_select_related = ("customer",)
    filter_horizontal = ("tags",)
    inlines = [CommentInline]
    ordering = ("-created_at", "-id")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("ticket", "author_name", "is_internal", "created_at")
    list_filter = ("is_internal", "created_at")
    search_fields = ("ticket__title", "author_name", "body")
    autocomplete_fields = ("ticket",)
