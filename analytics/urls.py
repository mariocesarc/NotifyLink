from django.urls import path

from analytics import views
from analytics.telegram_webhook import telegram_webhook


urlpatterns = [
    path('click/<uuid:link_uuid>/', views.count_link_click, name='count_link_click'),
    path('telegram/webhook/', telegram_webhook, name='telegram_webhook'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
