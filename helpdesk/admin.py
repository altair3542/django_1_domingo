from django.contrib import admin
from .models import Comment, Customer, Tag, Ticket


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "email")
    search_fields = ("name", "email")
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


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("title", "customer", "status", "priority", "created_at")
    search_fields = ("title", "customer__name", "customer__email")
    list_filter = ("status", "priority", "tags")
    list_select_related = ("customer",)
    autocomplete_fields = ("customer",)
    filter_horizontal = ("tags",)
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("ticket", "author_name", "is_internal", "created_at")
    list_filter = ("is_internal",)
    search_fields = ("ticket__title", "author_name", "body")
    autocomplete_fields = ("ticket",)
