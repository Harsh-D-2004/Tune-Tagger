from django.db import models
import uuid

class Video(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING' , 'PENDING'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video_file = models.FileField(upload_to='videos/' , default=None)
    extracted_audio_file = models.FileField(upload_to='audio/' , default=None , max_length=1000)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.video_file} - {self.status}"
    
class YTVideo(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING' , 'PENDING'
        PROCESSING = 'PROCESSING', 'Processing'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    video_file_link = models.CharField(max_length=10000 , blank=False)
    extracted_audio_file = models.FileField(upload_to='audio/' , default=None)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"{self.video_file_link} - {self.status}"