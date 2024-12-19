from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import uuid
import os

from usersystem.usermodel import DiaryUser

def unique_image_path(instance, filename):
    # Получаем расширение исходного файла
    ext = filename.split('.')[-1]
    # Создаём уникальное имя с помощью UUID
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    # Дополнительно можно использовать логическую структуру каталогов
    return os.path.join("images/emotionicons", unique_name)

class Emotion(models.Model):
    name = models.CharField(max_length=64) # название эмоции
    description = models.TextField(null=True) # её описание, синонимы и т.д.
    rating = models.PositiveSmallIntegerField( # численная оценка настроения, стоящая за иконкой
    validators=[MinValueValidator(1), MaxValueValidator(10)]) # ограничивает значения от 1 до 10
    imageIcon = models.ImageField(null=True, upload_to=unique_image_path)
    owner = models.ForeignKey(DiaryUser, on_delete=models.CASCADE, default=None, null=True, blank=True) # кому принадлежит эмоция
    # None -> доступно всем

    def __str__(self):
        return self.name

