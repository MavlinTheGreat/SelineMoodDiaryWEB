from django.db import models
from django.utils import timezone

from .emotions import Emotion
from .notetags import NoteTag
from usersystem.usermodel import DiaryUser


class EmotionNote(models.Model):
    date = models.DateTimeField(default=timezone.now) # дата отметки
    emotion = models.ForeignKey(Emotion, on_delete=models.SET_NULL, related_name="notes", null=True) # эмоция
    content = models.TextField(null=True) # содержимое заметки
    user = models.ForeignKey(DiaryUser, on_delete=models.CASCADE) # автор
    tags = models.ManyToManyField(NoteTag, related_name="notes")