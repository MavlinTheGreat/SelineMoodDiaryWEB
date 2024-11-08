from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from selinemooddiary.usersystem.usermodel import DiaryUser


class Emotion(models.Model):
    name = models.CharField() # название эмоции
    description = models.TextField() # её описание, синонимы и т.д.
    rating = models.PositiveSmallIntegerField( # численная оценка настроения, стоящая за иконкой
        validators=[MinValueValidator(1), MaxValueValidator(10)]) # ограничивает значения от 1 до 10
    imageIcon = models.FileField()
    owner = models.ForeignKey(DiaryUser, on_delete=models.CASCADE, default=None)

