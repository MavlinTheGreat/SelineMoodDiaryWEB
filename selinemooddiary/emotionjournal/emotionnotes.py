from django.db import models
from django.utils import timezone

from selinemooddiary.emotionjournal.emotions import Emotion
from selinemooddiary.usersystem.usermodel import DiaryUser


class EmotionNote(models.Model):
    date = models.DateTimeField(default=timezone.now)
    emotion = models.ForeignKey(Emotion, on_delete=models.SET_NULL)
    content = models.TextField()
    user = models.ForeignKey(DiaryUser, on_delete=models.CASCADE)