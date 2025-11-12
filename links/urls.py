from django.urls import path

from links import views


urlpatterns = [
    path('config/', views.config_page, name='config_page'),
    path('config/profile/update/', views.update_profile, name='update_profile'),
    path('config/telegram/connect/', views.telegram_connect, name='telegram_connect'),
    path('config/telegram/check/', views.telegram_check, name='telegram_check'),
    path('config/telegram/disconnect/', views.telegram_disconnect, name='telegram_disconnect'),
    path('config/links/add/', views.add_link, name='add_link'),
    path('config/links/<uuid:link_id>/delete/', views.delete_link, name='delete_link'),
    path('config/links/<uuid:link_id>/toggle/', views.toggle_link, name='toggle_link'),
    path('config/links/<uuid:link_id>/move/', views.move_link, name='move_link'),
    path('config/links/<uuid:link_id>/update/', views.update_link, name='update_link'),
    path('<str:username>/', views.get_user_page, name='get_user_page'),
]
