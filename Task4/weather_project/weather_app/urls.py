from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    # path('weather/<str:city>', views.weather, name='weather'),
]