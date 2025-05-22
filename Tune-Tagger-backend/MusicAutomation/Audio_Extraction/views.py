from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.shortcuts import render
from .serializers import VideoSerializer , YTVideoSerializer
from rest_framework import views , response , status
from .models import Video , YTVideo
import ffmpeg
import os
import shutil
import yt_dlp

class VideoViews(views.APIView):

    def post(self, request):
        serializer = VideoSerializer(data=request.data)
        if serializer.is_valid():
            video_instance = serializer.save()
            self.convert_video_to_audio(video_instance)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self , request , id=None):

        if id:
            video_instance = Video.objects.get(id = id)
            serializer = VideoSerializer(video_instance)
            return response.Response(serializer.data)
        else:
            videos = Video.objects.all()
            if(videos.count() == 0):
                return response.Response({ "message": _("No videos found")}, status=status.HTTP_200_OK)
            serializer = VideoSerializer(videos , many=True)
            return response.Response(serializer.data)
    
    def put(self , request , id):

        try:
            video_instance = Video.objects.get(id=id)
        except Video.DoesNotExist:
            return response.Response(
                { "message": _("Video not found")}, 
                status=status.HTTP_404_NOT_FOUND)

        if video_instance == None:
            return response.Response({ "message": _("Video not found")}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = VideoSerializer(video_instance , data = request.data , partial = True)
        if serializer.is_valid():
            video_instance = serializer.save()
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request , id=None):

        if id:
            video_instance = Video.objects.get(id = id)

            if video_instance == None:
                return response.Response({ "message": _("Video not found")}, status=status.HTTP_404_NOT_FOUND)
            
            video_instance.delete()
            return response.Response({ "message": _("Video deleted successfully")}, status=status.HTTP_204_NO_CONTENT)
        else:
            try:
                audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio/')
                video_dir = os.path.join(settings.MEDIA_ROOT, 'videos/')
                if not os.path.exists(video_dir):
                    os.makedirs(video_dir, exist_ok=True)
                   
                shutil.rmtree(audio_dir)
                shutil.rmtree(video_dir)
                return response.Response({ "message": _("Video and Audio directory deleted successfully")}, status=status.HTTP_200_OK)
            except Exception as e:
                return response.Response({"error": str(e)} , status = status.HTTP_400_BAD_REQUEST)
    
    def convert_video_to_audio(self, video):
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio/')
        os.makedirs(audio_dir, exist_ok=True)

        video_file = os.path.join(settings.MEDIA_ROOT, video.video_file.name)

        base_filename = os.path.basename(video.video_file.name)

        audio_file = os.path.join(audio_dir, f"{os.path.splitext(base_filename)[0]}.wav")

        try:
            print(f"Converting {video_file} to {audio_file}...")
            ffmpeg.input(video_file).output(audio_file, format='wav').run()
        except ffmpeg.Error as e:
            print("FFmpeg error:")
            raise
        except Exception as e:
            print("Unexpected error:", str(e))
            raise

        relative_audio_path = os.path.relpath(audio_file, settings.MEDIA_ROOT)
        video.extracted_audio_file = relative_audio_path
        video.status = Video.Status.COMPLETED.name 
        video.save()

class YoutubeView(views.APIView):

    def post(self, request):
        serializer = YTVideoSerializer(data = request.data)
        if serializer.is_valid():
            YTVideo_instance = serializer.save()
            video_instance = self.yt_to_wav(YTVideo_instance)
            serialized_video = VideoSerializer(video_instance)
            return response.Response(serialized_video.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def yt_to_wav(self , YTVideo_instance):

        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audio/')

        downloaded_file_path = {}

        def my_hook(d):
            if d['status'] == 'finished':
                downloaded_file_path['path'] = d['filename']

        ydl_opts = { "format": "bestaudio",
            'postprocessors': [{ "key": "FFmpegExtractAudio", "preferredcodec": "wav",  
            }],
            'outtmpl': os.path.join(audio_dir, '%(title)s.%(ext)s'),
            'progress_hooks': [my_hook],
        }

        video_url = YTVideo_instance.video_file_link

        try:
        
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading audio from: {video_url}")
                ydl.download([video_url])
                print("Download completed!")

                original_path = downloaded_file_path.get('path')
                base_name, _ = os.path.splitext(original_path)  # Strip the original extension
                final_path = f"{base_name}.wav"
                relative_path = os.path.relpath(final_path, settings.MEDIA_ROOT)
                YTVideo_instance.status = YTVideo.Status.COMPLETED.name 
                YTVideo_instance.extracted_audio_file = relative_path
                YTVideo_instance.save()

                video_instance = Video.objects.create(                    
                    # video_file = video_url,
                    extracted_audio_file = relative_path,
                    status = Video.Status.COMPLETED.name
                )

                return video_instance


        except Exception as e:
            print("Unexpected error:", str(e))
            YTVideo_instance.status = YTVideo.Status.FAILED.name
            YTVideo_instance.save()
            raise