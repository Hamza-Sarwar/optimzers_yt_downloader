# downloader/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('download-channel/', views.download_channel, name='download_channel'),
    path('download-video/', views.download_video, name='download_video'),
    path('download-playlist/', views.download_playlist, name='download_playlist'),
]