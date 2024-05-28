from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Exemple de vue pour la page d'accueil
    path('result/', views.result, name='result'),
    path('localize/', views.localize, name='localize'),
    path('map/', views.map, name='map'),
    # Autres schémas d'URL...
]
