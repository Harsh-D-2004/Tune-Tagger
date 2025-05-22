from django.urls import path
from .views import AudioChunkView

urlpatterns =[
    path('audio-chunks/', AudioChunkView.as_view(), name='audio_chunk'),
    path('audio-chunks/delete/', AudioChunkView.as_view(), name='delete_chunks_database'),
]