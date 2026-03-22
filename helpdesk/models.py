from django.db import models
from django.db.models import Q
from django.core.validators import MinLengthValidator

# Create your models here.
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Customer(TimeStampedModel):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    company = models.CharField(max_length=120, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.name} <{self.email}>"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)

    class Meta:
        ordering = ["name"]

class Ticket(TimeStampedModel):
    class Status(models.TextChoices):
        OPEN = "open", "Abierto"
        IN_PROGRESS = "in_progress", "En progreso"
        CLOSED = "closed", "Cerrado"

    class Priority(models.IntegerChoices):
        LOW = 1, "Bajo"
        MEDIUM = 2, "Medio"
        HIGH = 3, "Alto"

    title = models.CharField(
        max_length=200,
        validators=[MinLengthValidator(8)]
    )
    description = models.TextField(blank=True)

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="tickets",
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
        db_index=True
    )

    priority = models.IntegerField(
        choices=Priority.choices,
        default=Priority.MEDIUM,
        db_index=True
    )

    tags = models.ManyToManyField(
        Tag,
        related_name="tickets",
        blank=True
    )

    class Meta:
        ordering = ["-created_at", "-id"]
        constraints = [
            models.CheckConstraint(
                condition=Q(title__regex=r".*\S.*"),
                name ="ticket_title_not_blank_only_spaces"
            )
        ]
        indexes = [
            models.Index(fields=["status", "priority"], name="ticket_status_priority_idx"),
            models.Index(fields=["customer", "-created_at"], name="ticket_customer_created_idx"),
        ]

    def __str__(self) -> str:
        return f"#{self.pk} - {self.title}"

class Comment(TimeStampedModel):
    ticket = models.ForeignKey(
        Ticket,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author_name = models.CharField(max_length=120)
    body = models.TextField(validators=[MinLengthValidator(3)])
    is_internal = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["ticket", "created_at"], name="comment_ticket_created_idx"),
        ]

    def __str__(self) -> str:
        return f"Comment({self.ticket_id}, {self.author_name})"
