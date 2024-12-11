from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from usersystem.usermodel import DiaryUser


class Emotion(models.Model):
    name = models.CharField(max_length=64) # название эмоции
    description = models.TextField(null=True) # её описание, синонимы и т.д.
    rating = models.PositiveSmallIntegerField( # численная оценка настроения, стоящая за иконкой
    validators=[MinValueValidator(1), MaxValueValidator(10)]) # ограничивает значения от 1 до 10
    imageIcon = models.ImageField(null=True, upload_to="images/emotionicons/")
    owner = models.ForeignKey(DiaryUser, on_delete=models.CASCADE, default=None, null=True) # кому принадлежит эмоция
    # None -> доступно всем

    def __str__(self):
        return self.name

    @property
    def is_global(self):
        """Проверка, является ли эмоция глобальной."""
        return self.owner is None