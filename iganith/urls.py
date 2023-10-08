from django.contrib import admin
from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('', views.iganithHome, name='iganithHome'),
    path('round1', views.ganith1, name='iganith1'),
    path('round2', views.ganith2, name='iganith2'),
]