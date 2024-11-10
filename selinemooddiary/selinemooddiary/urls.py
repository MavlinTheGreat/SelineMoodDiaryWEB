from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from usersystem import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('about/', include('projectinfo.urls')),
    path('about/', TemplateView.as_view(template_name="index.html")),
    path('login/', auth_views.LoginView.as_view()),
    path('auth/', auth_views.RegistrationView.as_view()),
    path('', TemplateView.as_view(template_name="index.html")),
]
