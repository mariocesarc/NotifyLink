from colorfield.fields import ColorField
from django.conf import settings
from django.db import models, transaction
from django.templatetags.static import static


class PageTheme(models.Model):
    
    class FontFamily(models.TextChoices):
        INTER = 'Inter', 'Inter'
        POPPINS = 'Poppins', 'Poppins'
        MONTSERRAT = 'Montserrat', 'Montserrat'
        ROBOTO = 'Roboto', 'Roboto'
        LORA = 'Lora', 'Lora'
        RALEWAY = 'Raleway', 'Raleway'
        SOURCE_SANS = 'Source Sans 3', 'Source Sans 3'
        PLAYFAIR = 'Playfair Display', 'Playfair Display'
        SPACE_GROTESK = 'Space Grotesk', 'Space Grotesk'
        DM_SANS = 'DM Sans', 'DM Sans'

    class BorderRadius(models.TextChoices):
        SHARP = '0px', 'Sharp (0px)'
        SLIGHT = '8px', 'Slight (8px)'
        ROUNDED = '16px', 'Rounded (16px)'
        PILL = '999px', 'Pill (fully rounded)'

    class LinkHeight(models.TextChoices):
        SMALL = 'p-2', 'Small'
        NORMAL = 'p-4', 'Normal'
        TALL = 'p-6', 'Tall'


    name = models.CharField(max_length=50, unique=True)

    blur_behind_bio = models.BooleanField(default=True)
    background_image = models.ImageField(upload_to='backgrounds/', blank=True, null=True)
    background_color = ColorField(default='#000000')
    avatar_outline_color = ColorField(default='#404040')
    text_color = ColorField(default='#C0C0C0')
    font_family = models.CharField(max_length=64, choices=FontFamily.choices, default=FontFamily.POPPINS)

    # links
    link_height = models.CharField(max_length=64, choices=LinkHeight.choices, default=LinkHeight.NORMAL)
    link_roundness = models.CharField(max_length=64, choices=BorderRadius.choices, default=BorderRadius.PILL)
    link_background_color = ColorField(default='#808080')
    link_outline_color = ColorField(default='#404040')
    link_hover_color = ColorField(default='#404040')
    link_text_color = ColorField(default='#ffffff')
    link_font_family = models.CharField(max_length=64, choices=FontFamily.choices, default=FontFamily.SPACE_GROTESK)

    def __str__(self):
        return self.name


class Link(models.Model):

    class Type(models.TextChoices):
        GENERIC = 'generic', 'Generic'
        INSTAGRAM = 'instagram', 'Instagram'
        FACEBOOK = 'facebook', 'Facebook'
        YOUTUBE = 'youtube', 'YouTube'
        TIKTOK = 'tiktok', 'TikTok'
        GITHUB = 'github', 'GitHub'

    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    type = models.CharField(max_length=32, choices=Type.choices, default=Type.GENERIC)
    name = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def icon_url(self):
        return static('icons/{}_icon.png'.format(self.type))

    def save(self, *args, **kwargs):
        if self._state.adding:
            # auto increment order for new links
            last_link = Link.objects.filter(user=self.user).order_by('-order').first()
            last_order = last_link.order if last_link else 0
            self.order = last_order + 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        with transaction.atomic():
            links = Link.objects.filter(user=user).order_by('order')
            for i, link in enumerate(links):
                link.order = i + 1
                link.save(update_fields=['order'])

    def move_to(self, new_position):

        links = list(Link.objects.filter(user=self.user).order_by('order'))

        if new_position < 1:
            new_position = 1

        if new_position > len(links):
            new_position = len(links)

        real_position = None
        for i, link in enumerate(links):
            if self.id == link.id:
                real_position = i + 1
                break

        current_link = links.pop(real_position - 1)
        links.insert(new_position - 1, current_link)

        with transaction.atomic():
            for i, link in enumerate(links):
                link.order = i + 1
                link.save(update_fields=['order'])

    def __str__(self):
        return '{} - {}'.format(self.user.username, self.name)
