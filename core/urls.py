from django.urls import path

from . import views


urlpatterns = [
    path('', views.auth_spotify, name='auth_spotify'),
    path('home/', views.home,  name='home'),
    
    
]