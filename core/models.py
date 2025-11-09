import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from links.models import PageTheme


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, blank=True, null=False)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    display_name = models.CharField(max_length=64, blank=True, null=False)
    bio = models.TextField(max_length=500, blank=True, null=False)
    page_theme = models.ForeignKey(to=PageTheme, on_delete=models.PROTECT)

    class Meta:
        ordering = ['-date_joined']

    def __str__(self):
        return self.username


class SubscriptionPlan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True, null=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    billing_cycle = models.CharField(max_length=64, default='monthly')

    def __str__(self):
        return self.name


class SubscriptionPayment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'pending'
        PAID = 'paid', 'paid'
        FAILED = 'failed', 'failed'
        REFUNDED = 'refunded', 'refunded'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.PROTECT)
    plan = models.ForeignKey(to=SubscriptionPlan, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    payment_reference = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.PENDING)

    class Meta:
        ordering = ['-paid_at']

    def __str__(self):
        return '{} - {} - ${}'.format(self.user.username, self.plan.name, self.amount)
