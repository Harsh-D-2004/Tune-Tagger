from rest_framework import serializers
from .models import AudioChunk

class AudioChunkSerializer(serializers.ModelSerializer):

    class Meta:
        model = AudioChunk
        fields = '__all__'