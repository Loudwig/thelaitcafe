from django.urls import path
from .views import shop,order_capsule,update,getTransaction


urlpatterns = [
    path('',shop, name = 'boutique'),
    path('order_capsule', order_capsule,name='order_capsule' ),
    path('getTransaction', getTransaction, name = 'getTransaction'),
    path('update',update, name = 'update'),
]

