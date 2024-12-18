from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticated
from .emotions import Emotion
from .emotionnotes import EmotionNote
from .notetags import NoteTag
from .serializers import EmotionSerializer, EmotionNoteSerializer, NotetagsSerializer
from django.db.models import Q


class EmotionNoteListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmotionNoteSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # Подключаем фильтрацию и сортировку
    filterset_fields = ['emotion', 'date']  # Поля для фильтрации
    ordering_fields = ['date']  # Поля для сортировки
    ordering = ['date']  # Сортировка по умолчанию: от старых к новым

    def get_queryset(self):
        # Возвращаем только заметки текущего пользователя
        res = EmotionNote.objects.filter(user=self.request.user)
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            res = res.filter(date__gte=start_date)
        if end_date:
            res = res.filter(date__lt=end_date)
        return res

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


class NoteTagListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = NotetagsSerializer

    def get_queryset(self):
        # Показываем только глобальные теги или эмоции текущего пользователя
        return NoteTag.objects.filter(Q(owner=None) | Q(owner=self.request.user))

    def perform_create(self, serializer):
        # Автоматически устанавливаем текущего пользователя как владельца тега
        serializer.save(owner=self.request.user)