from django.contrib import admin
from analytics.models import LinkClick, ClickNotification


@admin.register(LinkClick)
class LinkClickAdmin(admin.ModelAdmin):
    list_display = ('link__user__username', 'link__name', 'ip_address', 'click_count', 'timestamp')


@admin.register(ClickNotification)
class ClickNotificationAdmin(admin.ModelAdmin):
    list_display = ('link__user__username', 'link__name', 'type', 'success', 'timestamp')
