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

GROUP_ICONS = {
        'HAP': ('STATIC/EMOTION_GROUPS/happy.webp', '#fbec5d'),
        'CALM': ('STATIC/EMOTION_GROUPS/calm.webp', '#00ff00'),
        'INDIF': ('STATIC/EMOTION_GROUPS/indiff.webp', '#bc8f8f'),
        'ANG': ('STATIC/EMOTION_GROUPS/angry.webp', '#ff6347'),
        'SAD': ('STATIC/EMOTION_GROUPS/sad.webp', '#629edd'),
        'OTH': ('STATIC/EMOTION_GROUPS/other.webp', '#c8c8c8') ,
}

class Emotion(models.Model):
    class EmotionGroup(models.TextChoices):
        HAPPY = 'HAP', 'Радость'
        CALM = 'CALM', 'Спокойствие'
        INDIFF = 'INDIF', 'Безразличие'
        ANGRY = 'ANG', 'Злость'
        SAD = 'SAD', 'Грусть'
        OTHER = 'OTH', 'Другое'

    name = models.CharField(max_length=64) # название эмоции
    description = models.TextField(null=True) # её описание, синонимы и т.д.
    rating = models.PositiveSmallIntegerField( # численная оценка настроения, стоящая за иконкой
    validators=[MinValueValidator(1), MaxValueValidator(10)]) # ограничивает значения от 1 до 10
    imageIcon = models.ImageField(null=True, upload_to=unique_image_path)
    owner = models.ForeignKey(DiaryUser, on_delete=models.CASCADE, default=None, null=True, blank=True) # кому принадлежит эмоция
    # None -> доступно всем
    group = models.CharField(  # группа эмоции
        max_length=20,
        choices=EmotionGroup.choices,
        default=EmotionGroup.OTHER,
        null=True
    )

    # получение иконки группы, к которой принадлежит эмоция
    def get_group_icon(self):
        return GROUP_ICONS.get(self.group, GROUP_ICONS['OTH'])[0]

    # получение цвета группы, к которой принадлежит эмоция (для графика круговой диаграммы)
    def get_group_color(self):
        return GROUP_ICONS.get(self.group, GROUP_ICONS['OTH'])[1]

    def __str__(self):
        return self.name

