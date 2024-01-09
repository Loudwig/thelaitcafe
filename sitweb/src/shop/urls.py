from django.urls import path
from .views import index,shop,order_capsule


urlpatterns = [
    path('',shop, name = 'boutique'),
    path('order_capsule', order_capsule,name='order_capsule' )
]

