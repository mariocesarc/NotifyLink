from colorfield.fields import ColorField
from django.conf import settings
from django.db import models


class PageTheme(models.Model):

    name = models.CharField(max_length=50, unique=True)

    background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    background_color = ColorField(default='#000000')
    text_color = ColorField(default='#808080')
    font_family = models.CharField(max_length=64, default='Roboto')

    # links
    link_background_color = ColorField(default='#808080')
    link_outline_color = ColorField(default='#404040')
    link_hover_color = ColorField(default='#404040')
    link_text_color = ColorField(default='#ffffff')
    link_font_family = models.CharField(max_length=64, default='Roboto')

    def __str__(self):
        return self.name


class Link(models.Model):

    class Type(models.TextChoices):
        GENERIC = 'generic', 'Generic'
        INSTAGRAM = 'instagram', 'Instagram'
        FACEBOOK = 'facebook', 'Facebook'
        YOUTUBE = 'youtube', 'YouTube'
        TIKTOK = 'tiktok', 'TikTok'

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    type = models.CharField(max_length=32, choices=Type.choices, default=Type.GENERIC)
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.name)
