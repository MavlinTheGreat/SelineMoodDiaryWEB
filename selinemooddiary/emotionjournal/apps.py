from django.apps import AppConfig
from django.db import IntegrityError


class EmotionjournalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emotionjournal'

    def ready(self):
        from .emotions import Emotion  # Импортируем модель
        default_emotions = [
            {"name": "Счастье", "description": "Положительное, радостное чувство", "rating": 8, "owner": None},
            {"name": "Грусть", "description": "Печальное, меланхоличное состояние", "rating": 2, "owner": None},
            {"name": "Удивление", "description": "Эмоция от неожиданности", "rating": 5, "owner": None},
        ]
        for emotion in default_emotions:
            try:
                Emotion.objects.get_or_create(name=emotion["name"], defaults=emotion)
            except IntegrityError:
                pass  # Обрабатываем случаи, если БД ещё недоступна (например, во время миграции)
