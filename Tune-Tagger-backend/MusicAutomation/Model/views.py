from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Chunking.models import AudioChunk
from .models import SongPreds
from rest_framework import views, response, status
import tensorflow as tf
import numpy as np
import pickle
import io
import http.client
from pydub import AudioSegment
import os
import base64
import json
from .serializers import SongPredsSerializers


class SongPredsView(views.APIView):
    model = tf.keras.models.load_model(
        "D:\\Auto time stamper and music detection\\music_detection_model.keras"
    )
    current_song = None

    def post(self, request):
        audio_chunks = AudioChunk.objects.all()
        self.current_song = ""
        print(self.model.summary)
        for audio_chunk in audio_chunks[:20]:
            spectrogram = self.extract_spectrogram(audio_chunk)

            self.predict(spectrogram, audio_chunk)

            self.song_finder(audio_chunk)

        return response.Response(
            {"Result": _("Successfully predicted")}, status=status.HTTP_201_CREATED
        )

    def get(self, request):
        preds = SongPreds.objects.all()
        if preds.count() == 0:
            return response.Response(
                {"message": _("No predictions found")}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = SongPredsSerializers(preds, many=True)
        return response.Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        try:
            SongPreds.objects.all().delete()
            return response.Response(
                {"message": _("Predictions deleted successfully")},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return response.Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    def extract_spectrogram(self, audio_chunk):
        try:
            binary_stream = io.BytesIO(audio_chunk.spectrogram_image)
            spectrogram = pickle.load(binary_stream)
            return spectrogram
        except Exception as e:
            return response.Response(
                {"error": f"Failed to deserialize spectrogram: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def predict(self, spectrogram, audio_chunk):
        spectrogram_input = np.array(spectrogram)

        spectrogram_input = np.expand_dims(spectrogram_input, axis=-1)
        spectrogram_input = np.expand_dims(spectrogram_input, axis=0)

        prediction = self.model.predict(spectrogram_input)
        predicted_class = np.argmax(prediction, axis=1)[0]
        audio_chunk.labels = predicted_class
        audio_chunk.save()

    def send_to_shazam(self, encoded_data):
        conn = http.client.HTTPSConnection("shazam-api-free.p.rapidapi.com")
        headers = {
            "x-rapidapi-key": "772354c8f6mshff6ce85382008e5p1be235jsn5cf1a16d5917",
            "x-rapidapi-host": "shazam.p.rapidapi.com",
            "Content-Type": "text/plain",
        }

        try:
            conn.request(
                "POST",
                "/shazam/recognize/",
                body=encoded_data,
                headers=headers,
            )
            res = conn.getresponse()
            if res.status != 200:
                return {"error": f"Failed with status code {res.status}: {res.reason}"}
            data = res.read()
            return data.decode("utf-8")
        except Exception:
            return "Failed to send to Shazam"

    def song_finder(self, audio_chunk):
        if audio_chunk.labels == 1:
            try:
                audio_path = os.path.join(
                    settings.MEDIA_ROOT, audio_chunk.chunk_file.name
                )
                encoded_data = self.convert_shortened_chunk_to_raw(audio_path)
                response_from_api = self.send_to_shazam(encoded_data)
                response_data = json.loads(response_from_api)

                detected_song = "Unknown"
                artist_name = "Unknown"
                # background_image = "Unknown"
                # shazam_link = "Unknown"
                track_data = response_data.get("track")
                if track_data:
                    detected_song = response_data["track"].get("title", "Unknown")
                    artist_name = track_data.get("subtitle", "Unknown")
                audio_chunk.song_prediction = detected_song
                audio_chunk.save()

                if detected_song != "Unknown" and detected_song != self.current_song:
                    self.current_song = detected_song
                    SongPreds.objects.create(
                        start_time=audio_chunk.start_time,
                        song_name=self.current_song,
                        artist_name=artist_name,
                    )

            except Exception as e:
                return response.Response(
                    {"Result": _("Error in Shazam API"), "exception": str(e)},
                    status=status.HTTP_204_NO_CONTENT,
                )

    def convert_shortened_chunk_to_raw(self, audio_path, duration_ms=3000):
        audio = AudioSegment.from_wav(audio_path)

        short_audio = audio[:duration_ms]

        short_audio = (
            short_audio.set_channels(1).set_frame_rate(44100).set_sample_width(2)
        )

        temp_dir_path = os.path.join(settings.MEDIA_ROOT, "temp")
        os.makedirs(temp_dir_path, exist_ok=True)
        temp_file_path = os.path.join(temp_dir_path, "temp.raw")
        short_audio.export(temp_file_path, format="raw")

        with open(temp_file_path, "rb") as raw_file:
            raw_data = raw_file.read()
        encoded_data = base64.b64encode(raw_data).decode("utf-8")

        os.remove(temp_file_path)

        return encoded_data
