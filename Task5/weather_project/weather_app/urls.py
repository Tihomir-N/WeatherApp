from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('?city=<str:city>', views.home, name='weather'),
]