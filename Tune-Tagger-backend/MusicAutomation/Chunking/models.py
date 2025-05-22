from django.db import models
from Audio_Extraction.models import Video
import uuid


class AudioChunk(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='audio_chunks')
    chunk_file = models.FileField(upload_to='chunks/' , blank=True, null=True)
    start_time = models.FloatField(blank=True, null=True)
    spectrogram_image = models.BinaryField(blank=True, null=True)
    labels = models.IntegerField(default=None , blank=True , null=True)
    song_prediction = models.CharField(max_length=200 , default = '', blank=True)