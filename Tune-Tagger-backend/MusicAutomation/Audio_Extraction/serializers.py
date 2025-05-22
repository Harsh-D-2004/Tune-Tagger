from rest_framework import serializers
from .models import Video , YTVideo


class VideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Video
        fields = '__all__'

class YTVideoSerializer(serializers.ModelSerializer):

    class Meta:
        model = YTVideo
        fields = '__all__'