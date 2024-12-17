from django.db import models
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .emotions import Emotion
from .notetags import NoteTag
from usersystem.usermodel import DiaryUser


class EmotionNote(models.Model):
    date = models.DateTimeField(default=timezone.now) # дата отметки
    emotion = models.ForeignKey(Emotion, on_delete=models.SET_NULL, related_name="notes", null=True) # эмоция
    content = models.TextField(null=True) # содержимое заметки
    user = models.ForeignKey(DiaryUser, on_delete=models.CASCADE) # автор
    tags = models.ManyToManyField(NoteTag, related_name="notes", blank=True)

    def clean(self):
        # Проверяем, что Emotion принадлежит либо всем (owner=None), либо текущему пользователю.
        if self.emotion and self.emotion.owner not in {None, self.user}:
            raise ValidationError("Эмоция может быть либо глобальной, либо принадлежать текущему пользователю.")

    def save(self, *args, **kwargs):
        #Вызываем метод clean перед сохранением.
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.date} {self.emotion}"
