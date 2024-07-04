from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
                path('upload/', views.upload_img_info, name='upload'),
                path('color/', views.fetch_top_colors, name='color'),
            ]  

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)