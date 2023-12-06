from django.urls import path
from .views import connexion,creation_compte
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('creation_compte',creation_compte, name = 'creation_compte'),
    path('connexion',connexion, name = 'connexion'),
    path('logout',LogoutView.as_view(),name = 'logout' )
    
]