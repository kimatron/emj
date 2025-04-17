from django.urls import path
from . import views
from portfolio.views import debug_media

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('albums/', views.album_list, name='album_list'),
    path('albums/<slug:slug>/', views.album_detail, name='album_detail'),
    path('debug-media/', debug_media, name='debug_media'),
    path('debug-db/', views.debug_db, name='debug_db'),
    path('debug-do/', views.debug_do, name='debug_do'),
]