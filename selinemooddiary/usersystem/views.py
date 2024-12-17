from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView
from rest_framework.decorators import api_view, permission_classes


#from .forms import LoginForm, RegistrationForm
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import DiaryUserSerializer, UserTokenObtainPairSerializer, RegisterSerializer
from .usermodel import DiaryUser


# устаревший код для версии до использования Rest Framework

# class LoginView(TemplateView):
#
#     # def get(self, request):
#     #     if not request.user.is_authenticated:
#     #         form = LoginForm()
#     #         return render(request, "usersystem/login.html", {'loginform': form})
#     #     return redirect("/about")
#
#     def post(self, request):
#         if not request.user.is_authenticated:
#             form = LoginForm(request.POST)
#             if form.is_valid():
#                 cleared_user = form.cleaned_data
#                 user = authenticate(email=cleared_user['email'], password=cleared_user['password'])
#                 if user is not None:
#                     login(request, user)
#                 else:
#                     render(request, "usersystem/login.html")
#
#         return redirect("/about")


# class RegistrationView(TemplateView):
#
#     # def get(self, request):
#     #     if not request.user.is_authenticated:
#     #         form = RegistrationForm()
#     #         return render(request, "usersystem/registration.html", {'regform': form})
#     #     return redirect("/about")
#
#     def post(self, request):
#         if not request.user.is_authenticated:
#             form = RegistrationForm(request.POST)
#             if form.is_valid():
#                 form.password_check()
#                 new_user = form.save(commit=False)
#                 new_user.set_password(form.cleaned_data['password'])
#                 new_user.save()
#         return redirect("/about")


####  ТУТ НАЧИНАЕТСЯ НАСТОЯЩИЙ КОД

# Класс для получения информации о текущем пользователе
class DiaryUserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Только для авторизованных

    def get(self, request):
        user = request.user # текущий пользователь - через request
        serializer = DiaryUserSerializer(user)
        return Response(serializer.data)

# Получение токена
class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer

# Регистрация
class RegisterView(generics.CreateAPIView):
    queryset = DiaryUser.objects.all() # получение объектов DiaryUser
    permission_classes = (AllowAny,) # Разрешение на доступ без авторизации
    serializer_class = RegisterSerializer

    # Создание пользователя
    # Чисто технически создание пользователя осуществляется в род. классе CreateAPIView, но мы его переопределяем ради логирования
    def create(self, request, *args, **kwargs):
        print("Получен запрос:", request.data)
        return super().create(request, *args, **kwargs)

# Как будто бы в итоге не использовалась?
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUser(request):
     print("aboba")
     if request.method == "GET":
         return Response({'response': request.user}, status=status.HTTP_200_OK)
     return Response({'response': None}, status=status.HTTP_400_BAD_REQUEST)