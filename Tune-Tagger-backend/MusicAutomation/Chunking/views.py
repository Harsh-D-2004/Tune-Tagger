from django.utils.translation import gettext_lazy as _
from django.shortcuts import render
from rest_framework import views , response , status
import numpy as np
import librosa
import pandas as pd
from django.conf import settings
import os
from Audio_Extraction.models import Video
from .serializers import AudioChunkSerializer
import soundfile as sf
from .models import AudioChunk
import io
import shutil
from django.db.models import Q
import pickle

class AudioChunkView(views.APIView):

    def post(self , request):
        serializer = AudioChunkSerializer(data = request.data)
        if serializer.is_valid():
            audio_chunk_instance = serializer.save()
            video_id = audio_chunk_instance.video_id
            video_instance = Video.objects.get(id=video_id)
            audio_file = os.path.join(settings.MEDIA_ROOT , video_instance.extracted_audio_file.name)
            chunks , sr = self.split_audio(audio_file)
            for i, (chunk, start) in enumerate(chunks):
                
                chunk_file_path = os.path.join(settings.MEDIA_ROOT, f"chunks/chunk_{i}.wav")
                os.makedirs(os.path.dirname(chunk_file_path), exist_ok=True)
                sf.write(chunk_file_path, chunk, sr)

                S_db = self.create_spectrogram(chunk, sr)

                spectrogram_binary = pickle.dumps(S_db)

                AudioChunk.objects.create(
                    video=video_instance,
                    chunk_file=f"chunks/chunk_{i}.wav",
                    start_time=start,
                    spectrogram_image = spectrogram_binary
                )

            self.clean()

            return response.Response(
                { "message": _("Audio chunks and spectrograms created successfully")},
                status=status.HTTP_201_CREATED
            )
        return response.Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
    def delete(self , request):

        chunk_file_path = os.path.join(settings.MEDIA_ROOT, "chunks")

        try:
            shutil.rmtree(chunk_file_path)

            AudioChunk.objects.all().delete()

            return response.Response({ "message": _("Chunks directory deleted successfully")}, status=status.HTTP_200_OK)

        except Exception as e:
            return response.Response({"error": str(e)} , status = status.HTTP_400_BAD_REQUEST)

    def clean(self):
        null_chunks = AudioChunk.objects.filter(
            Q(video_id__isnull=True) |
            Q(chunk_file__isnull=True) |
            Q(start_time__isnull=True) |
            Q(spectrogram_image__isnull=True) |
            Q(chunk_file="") |
            Q(spectrogram_image=b"")
        )
        null_chunks.delete()
    

    def split_audio(self , audio_file, chunk_duration=20):
        y, sr = librosa.load(audio_file)
        total_duration = librosa.get_duration(y=y, sr=sr)
        chunks = []
        for i in range(0, int(total_duration), chunk_duration):
            start = i
            end = min(i + chunk_duration, total_duration)
            chunk = y[int(start * sr): int(end * sr)]
            chunks.append((chunk, start))
        return chunks, sr
    
    def get(self, request):
        
        chunks = AudioChunk.objects.all()

        if(chunks.count() == 0):
            return response.Response({ "message": _("No chunks found")}, status=status.HTTP_404_NOT_FOUND)
        
        serialzer = AudioChunkSerializer(chunks , many=True)
        return response.Response(serialzer.data , status=status.HTTP_200_OK)


    def create_spectrogram(self, chunk, sr ,  target_shape=(128, 128)):

        S = librosa.stft(chunk)
        S_db = librosa.amplitude_to_db(np.abs(S))

        if S_db.shape[1] < target_shape[1]:
            S_db = np.pad(S_db, ((0, 0), (0, target_shape[1] - S_db.shape[1])), mode='constant')
        elif S_db.shape[1] > target_shape[1]:
            S_db = S_db[:, :target_shape[1]]
                
        S_db = S_db[:target_shape[0], :target_shape[1]]

        return S_db