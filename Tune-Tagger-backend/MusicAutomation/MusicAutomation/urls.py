
from django.contrib import admin
from django.urls import path
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('preprocessing/' , include('Audio_Extraction.urls')),
    path('chunking/' , include('Chunking.urls')),
    path('model/' , include('Model.urls'))
]
