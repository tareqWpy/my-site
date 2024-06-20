from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class RegisterForm(UserCreationForm):
    captcha = CaptchaField()

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        )


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email / Username")
