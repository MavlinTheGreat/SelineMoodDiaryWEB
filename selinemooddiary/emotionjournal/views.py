from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .emotions import Emotion
from .emotionnotes import EmotionNote
from .serializers import EmotionSerializer, EmotionNoteSerializer
from django.db.models import Q


class EmotionNoteListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmotionNoteSerializer

    def get_queryset(self):
        # Возвращаем только заметки текущего пользователя
        return EmotionNote.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Автоматически устанавливаем пользователя как автора заметки
        serializer.save(user=self.request.user)


class EmotionNoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmotionNoteSerializer

    def get_queryset(self):
        # Возвращаем только заметки текущего пользователя
        return EmotionNote.objects.filter(user=self.request.user)


class EmotionListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmotionSerializer

    # список доступных эмоций
    def get_queryset(self):
        # Показываем только глобальные эмоции или эмоции текущего пользователя
        return Emotion.objects.filter(Q(owner=None) | Q(owner=self.request.user))

    def perform_create(self, serializer):
        # Автоматически устанавливаем текущего пользователя как владельца эмоции
        serializer.save(owner=self.request.user)


class EmotionDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmotionSerializer

    def get_queryset(self):
        # Разрешаем доступ только к глобальным эмоциям или эмоциям текущего пользователя
        return Emotion.objects.filter(owner__in=[None, self.request.user])
