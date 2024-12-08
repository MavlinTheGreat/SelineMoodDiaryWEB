from django.contrib.auth.password_validation import validate_password
from django.core.serializers import serialize
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .usermodel import DiaryUser

# Сериализатор для модели DiaryUser, который автоматически сериализует все поля модели
class DiaryUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiaryUser
        fields = '__all__'

# господи пусть чёрный с индусским акцентом с ютуба действительно поможет
class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user) # получение токена
        # Добавляем пользовательские поля из объекта user
        token['email'] = user.email
        token['account_status'] = user.account_status
        token['birthday'] = user.birthday.strftime('%Y-%m-%d') if user.birthday else None
        token['username'] = user.username

        return token

# Приём данных для регистрации
class RegisterSerializer(serializers.ModelSerializer):
    # пароль. write_only=True -> доп. поля не используется для создания объекта DiaryUser
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_repeat = serializers.CharField(
        write_only=True, required=True
    )

    class Meta:
        model = DiaryUser
        fields = ['email', 'username', 'birthday', 'password', 'password_repeat']

    # проверка на соответствие пароля и повторённого пароля
    def validate(self, attr):
        if attr['password'] != attr['password_repeat']:
            raise serializers.ValidationError(
                {"password": "Пароли не совпадают"}
            )
        return attr

    # создание пользователя
    def create(self, validated_data):
        user = DiaryUser.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            birthday=validated_data['birthday']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user