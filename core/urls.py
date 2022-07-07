from django.urls import path

from . import views


urlpatterns = [
    path('', views.authenticate, name='auth_spotify'),
    path('home/', views.home,  name='home'),
    
    
]