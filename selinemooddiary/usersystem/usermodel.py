from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionManager


class DiaryUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30, unique=True) # системный никнейм
    username = models.CharField(max_length=30) # отображаемое имя
    birthday = models.DateField(blank=True)
    account_status = models.CharField(max_length=10) # UNCHECKED - USER - AUTHOR - ADMIN
    selin = models.FileField(unique=True)


