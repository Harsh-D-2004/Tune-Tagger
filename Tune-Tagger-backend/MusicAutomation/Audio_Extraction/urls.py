from django.urls import path
from .views import VideoViews , YoutubeView

urlpatterns = [
    path('videos/', VideoViews.as_view(), name='video_list'),     
    path('videos/<uuid:id>/', VideoViews.as_view(), name='video_detail'), 
    path('youtube_video/', YoutubeView.as_view(), name='ytvideo_list'),
]