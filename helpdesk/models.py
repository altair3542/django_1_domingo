from django.db import models
from django.db.models import Count, Q


class Customer(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class TicketQuerySet(models.QuerySet):
    def with_related_for_listing(self):
        return self.select_related("customer").prefetch_related("tags")

    def with_comment_count(self):
        return self.annotate(comment_count=Count("comments", distinct=True))

    def ordered_for_listing(self):
        return self.order_by("-created_at", "-id")

    def by_status(self, status: str | None):
        if status:
            return self.filter(status=status)
        return self

    def by_priority(self, priority: str | int | None):
        if priority not in (None, ""):
            return self.filter(priority=priority)
        return self

    def by_tag(self, tag_slug: str | None):
        if tag_slug:
            return self.filter(tags__slug=tag_slug).distinct()
        return self

    def filter_by_params(self, *, status=None, priority=None, tag=None):
        return self.by_status(status).by_priority(priority).by_tag(tag)


class Ticket(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In Progress"
        CLOSED = "closed", "Closed"

    class Priority(models.IntegerChoices):
        LOW = 1, "Low"
        MEDIUM = 2, "Medium"
        HIGH = 3, "High"

    title = models.CharField(max_length=200)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name="tickets")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, db_index=True)
    priority = models.IntegerField(choices=Priority.choices, default=Priority.MEDIUM, db_index=True)
    tags = models.ManyToManyField(Tag, related_name="tickets", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = TicketQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at", "-id"]
        constraints = [
            models.CheckConstraint(
                condition=~Q(title=""),
                name="ticket_title_not_empty",
            )
        ]
        indexes = [
            models.Index(fields=["status", "priority"], name="ticket_status_priority_idx"),
            models.Index(fields=["customer", "created_at"], name="ticket_customer_created_idx"),
        ]

    def __str__(self) -> str:
        return f"[{self.get_status_display()}] {self.title}"


class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="comments")
    author_name = models.CharField(max_length=120)
    body = models.TextField()
    is_internal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at", "id"]
        indexes = [
            models.Index(fields=["ticket", "created_at"], name="comment_ticket_created_idx"),
        ]

    def __str__(self) -> str:
        return f"Comentario de {self.author_name} en ticket #{self.ticket_id}"
