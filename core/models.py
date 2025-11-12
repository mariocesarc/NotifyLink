import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    display_name = models.CharField(max_length=64, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    page_theme = models.ForeignKey(to='PageTheme', on_delete=models.PROTECT, blank=True, null=True)

    current_plan = models.ForeignKey(to='SubscriptionPlan', on_delete=models.PROTECT, blank=True, null=True)
    notifications_enabled = models.BooleanField(default=True)
    remaining_notifications = models.PositiveIntegerField(default=0)
    telegram_chat_id = models.CharField(max_length=64, blank=True)
    telegram_token = models.CharField(max_length=64, blank=True)
    token_expires = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-date_joined']

    def save(self, *args, **kwargs):
        # new instance: add default page_theme and default current_plan
        if self._state.adding:
            if self.page_theme_id is None:
                from links.models import PageTheme
                self.page_theme = PageTheme.get_default()
            if self.current_plan_id is None:
                self.current_plan = SubscriptionPlan.get_default()
                self.remaining_notifications = self.current_plan.max_notifications
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class SubscriptionPlan(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64, unique=True)
    description = models.TextField(blank=True)
    max_notifications = models.PositiveIntegerField(default=200)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    billing_cycle = models.CharField(max_length=64, default='monthly')
    active = models.BooleanField(default=True)

    @classmethod
    def get_default(cls):
        plan, _ = cls.objects.get_or_create(name='Free')
        return plan

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
