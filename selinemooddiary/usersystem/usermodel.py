from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionManager, PermissionsMixin


class DiaryUserManager(BaseUserManager):

    def create_user(self, email, nickname, username="Друг", password=None, birthday=None, **extra_fields):
        if not email:
            raise ValueError('Не предоставлен email')
        if not nickname:
            raise ValueError('Не предоставлен nickname')
        if not password:
            raise ValueError('Не предоставлен password')
        if len(password) < 8 or len(set(('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')).intersection(set(password))) == 0:
            raise ValueError('Слабый пароль')
        email = self.normalize_email(email)
        selin = None
        user = self.model(email=email, nickname=nickname, username=username, birthday=birthday, selin=selin, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, username="Друг", password=None, birthday=None, **extra_fields):
        extra_fields.setdefault('account_status', "ADMIN")
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        return self.create_user(email, nickname, username, password, birthday, **extra_fields)


class DiaryUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=30, unique=True) # системный никнейм
    username = models.CharField(max_length=30, default="Пользователь") # отображаемое имя
    birthday = models.DateField(null=True, blank=True)
    account_status = models.CharField(max_length=10, default="UNCHECKED") # UNCHECKED - USER - AUTHOR - ADMIN
    selin = models.FileField()

    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname']


    objects = DiaryUserManager()

    def __str__(self):
        return self.email

