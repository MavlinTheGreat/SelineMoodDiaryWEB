from django.http import HttpRequest, HttpResponse
from django.urls import path, include

urlpatterns = [
    path('', lambda request: HttpResponse('200')),
]