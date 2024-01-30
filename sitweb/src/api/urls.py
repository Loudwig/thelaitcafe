from django.urls import path
from .views import update,getTransaction,api_login


urlpatterns = [
    path('getTransaction', getTransaction, name = 'getTransaction'),
    path('update',update, name = 'update'),
    path('login',api_login, name = 'api_login')
]