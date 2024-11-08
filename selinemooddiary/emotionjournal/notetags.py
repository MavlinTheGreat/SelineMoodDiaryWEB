from django.db import models

from usersystem.usermodel import DiaryUser


class NoteTag(models.Model):
    name = models.CharField(max_length=64) # название тега
    icon = models.ImageField(null=True) # иконка
    desc = models.TextField(null=True) # описание
    owner = models.ForeignKey(DiaryUser, on_delete=models.CASCADE, default=None) # кому принадлежит тег
    # None -> доступно всем

    def __str__(self):
        return self.name