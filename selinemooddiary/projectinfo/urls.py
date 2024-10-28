from django.http import HttpRequest, HttpResponse
from django.urls import path, include
from .views import index

urlpatterns = [
    path('', index),
]