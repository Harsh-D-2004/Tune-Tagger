# Generated by Django 5.1.3 on 2024-11-26 20:28

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Audio_Extraction', '0003_rename_original_video_video_video_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='YTVideo',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('video_file_link', models.CharField(max_length=10000)),
                ('extracted_audio_file', models.FileField(default=None, upload_to='audio/')),
                ('status', models.CharField(choices=[('PENDING', 'PENDING'), ('PROCESSING', 'Processing'), ('COMPLETED', 'Completed'), ('FAILED', 'Failed')], default='PENDING', max_length=10)),
            ],
        ),
    ]
