from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView


class LoginView(TemplateView):

    def get(self, request):
        if request.session.get("user", None) is None:
            return render(request, "usersystem/login.html")
        return redirect("/about")

    def post(self, request):
        pass

class RegistrationView(TemplateView):

    def get(self, request):
        if request.session.get("user", None) is None:
            return render(request, "authentification.html")
        return redirect("/about")

    def post(self, request):
        pass