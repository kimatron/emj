from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('albums/', views.album_list, name='album_list'),
    path('albums/<slug:slug>/', views.album_detail, name='album_detail'),
]