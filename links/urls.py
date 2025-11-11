from django.urls import path
from links import views


urlpatterns = [
    path('<str:username>/', views.get_user_page, name='get_user_page'),
]
