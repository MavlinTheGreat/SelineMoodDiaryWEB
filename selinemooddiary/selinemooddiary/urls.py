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
    # авторизация
    path('api/user/', auth_views.DiaryUserDetailAPIView.as_view(), name="user_detail"), # информация о пользователе ???
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', auth_views.RegisterView.as_view()),
    # дневник эмоций
    path('api/journal/emotions', journal_views.EmotionListCreateView.as_view()),
    path('api/journal/emotions/<int:pk>', journal_views.EmotionDetailView.as_view()),
    path('api/journal/notes', journal_views.EmotionNoteListCreateView.as_view()),
    path('api/journal/notes/<int:pk>', journal_views.EmotionNoteDetailView.as_view()),
    path('api/journal/tags', journal_views.NoteTagListCreateView.as_view()),
    path('api/journal/tags/<int:pk>', journal_views.NoteTagDetailView.as_view())
]

if settings.DEBUG:  # Только для разработки
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)