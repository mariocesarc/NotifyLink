from django.urls import path

from core import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('sign_up/', views.sign_up, name='sign_up'),
    path('sign_in/', views.sign_in, name='sign_in'),
    path('logout/', views.log_out, name='logout'),
]
