from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from places import views
from places.views import get_place

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('places/<int:place_id>/', get_place, name='get_place'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
