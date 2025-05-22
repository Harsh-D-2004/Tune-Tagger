import uuid
from django.db import models


class SongPreds(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    start_time = models.FloatField(blank=True, null=True)
    song_name = models.CharField(max_length=200, blank=True, default='')
    artist_name = models.CharField(max_length=200, blank=True, default='')
