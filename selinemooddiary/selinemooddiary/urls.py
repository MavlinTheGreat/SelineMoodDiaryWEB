from django.contrib import admin
from django.urls import path, include
from usersystem import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', include('projectinfo.urls')),
    path('login/', auth_views.LoginView.as_view()),
    path('auth/', auth_views.RegistrationView.as_view()),
    path('', include('frontend_common.urls')),
]
