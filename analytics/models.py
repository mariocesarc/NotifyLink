import uuid

from django.db import models
from links.models import Link


class LinkClick(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    link = models.ForeignKey(to=Link, on_delete=models.CASCADE)
    click_count = models.PositiveIntegerField(default=1)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']


class ClickNotification(models.Model):

    class Type(models.TextChoices):
        TELEGRAM = 'telegram', 'Telegram'
        WHATSAPP = 'whatsapp', 'Whatsapp'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=32, choices=Type.choices, default=Type.TELEGRAM)
    link = models.ForeignKey(to=Link, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)

    class Meta:
        ordering = ['-timestamp']
