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
    return os.path.join("images/tagicons", unique_name)

class NoteTag(models.Model):
    name = models.CharField(max_length=64) # название тега
    icon = models.ImageField(null=True, upload_to=unique_image_path, blank=True) # иконка
    desc = models.TextField(null=True) # описание
    owner = models.ForeignKey(DiaryUser, on_delete=models.CASCADE, default=None, null=True, blank=True)  # кому принадлежит тег
    # None -> доступно всем

    def __str__(self):
        return self.name