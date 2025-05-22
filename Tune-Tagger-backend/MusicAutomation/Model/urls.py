from django.urls import path
from .views import SongPredsView

urlpatterns = [
    path('song-predictions/', SongPredsView.as_view(), name='song_predictions'),
]