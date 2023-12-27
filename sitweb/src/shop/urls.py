from django.urls import path
from .views import index,shop


urlpatterns = [
    path('',shop, name = 'boutique'),
]

