from django.urls import path
from .views import index,shop
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('',shop, name = 'boutique'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)