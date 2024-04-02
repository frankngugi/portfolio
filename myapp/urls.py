from django.urls import path, include
from . import views
from django.contrib import admin
from django.contrib.auth.views import LogoutView, LoginView




urlpatterns = [
    path('', views.index, name= 'index'),
    path('gallery', views.gallery, name= 'gallery'),
    path('chats', views.chats, name= 'chats'),
    path('register', views.register, name='register' ),
    path('login', views.login, name='login' ),
    path('logout', views.logout, name='logout'),
    path('videos', views.videos, name='videos'),
    path('videos', views.videos, name='videos'),
    path('profile', views.profile, name='profile'),
    path('change_password', views.change_password, name='change_password'),

]