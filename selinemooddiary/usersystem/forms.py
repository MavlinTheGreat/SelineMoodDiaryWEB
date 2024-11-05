from django import forms

from .usermodel import DiaryUser


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = DiaryUser
        fields = ["email", "nickname", "username", "birthday"]

    def password_check(self):
        cleared_user = self.cleaned_data
        if cleared_user['password'] != cleared_user['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cleared_user['password2']