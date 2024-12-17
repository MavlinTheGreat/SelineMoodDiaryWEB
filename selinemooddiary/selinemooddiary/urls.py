from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from usersystem import views as auth_views
from emotionjournal import views as journal_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('about/', include('projectinfo.urls')),
    # path('about/', TemplateView.as_view(template_name="index.html")),
    # path('login/', auth_views.LoginView.as_view()),
    # path('register/', auth_views.RegistrationView.as_view()),
    # path('', TemplateView.as_view(template_name="index.html")),
    path('api/user/', auth_views.DiaryUserDetailAPIView.as_view(), name="user_detail"), # информация о пользователе ???
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', auth_views.RegisterView.as_view()),
    path('api/journal/emotions', journal_views.EmotionListCreateView.as_view()),
    path('api/journal/notes', journal_views.EmotionNoteListCreateView.as_view())
]

if settings.DEBUG:  # Только для разработки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)