from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from accounts.views import CustomPasswordResetConfirmView, CustomPasswordResetView

from .views import *

app_name = "accounts"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("signup", signup_view, name="signup"),
    path(
        "activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        activate,
        name="activate",
    ),
    path(
        "password_reset/",
        CustomPasswordResetView.as_view(
            template_name="accounts/password_reset_form.html",
            email_template_name="accounts/password_reset_email.html",
            success_url=reverse_lazy("accounts:login"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset_confirm/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
]
