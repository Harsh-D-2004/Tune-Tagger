from rest_framework import serializers
from .models import SongPreds

class SongPredsSerializers(serializers.ModelSerializer):

    class Meta:
        model = SongPreds
        fields = '__all__'