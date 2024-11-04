from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView
from .forms import LoginForm, RegistrationForm


class LoginView(TemplateView):

    def get(self, request):
        if not request.user.is_authenticated:
            form = LoginForm()
            return render(request, "usersystem/login.html", {'loginform': form})
        return redirect("/about")

    def post(self, request):
        if not request.user.is_authenticated:
            form = LoginForm(request.POST)
            if form.is_valid():
                cleared_user = form.cleaned_data
                user = authenticate(email=cleared_user['email'], password=cleared_user['password'])
                if user is not None:
                    login(request, user)
                else:
                    render(request, "usersystem/login.html")

        return redirect("/about")


class RegistrationView(TemplateView):

    def get(self, request):
        if not request.user.is_authenticated:
            form = RegistrationForm()
            return render(request, "usersystem/registration.html", {'regform': form})
        return redirect("/about")

    def post(self, request):
        if not request.user.is_authenticated:
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.password_check()
                new_user = form.save(commit=False)
                new_user.set_password(form.cleaned_data['password'])
                new_user.save()
        return redirect("/about")
