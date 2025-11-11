from django.contrib import admin
from links.models import PageTheme, Link


@admin.register(PageTheme)
class PageThemeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'type', 'is_active', 'created_at')
    search_fields = ('user__username', 'user__email')
