from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from accounts.forms import RegisterForm
from accounts.models import CustomUser
from accounts.tokens import account_activation_token


def login_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    if "next" in request.POST:
                        messages.success(request, "You logged in successfully! 😀")
                        return redirect(request.POST.get("next"))
                    else:
                        messages.success(request, "You logged in successfully! 😀")
                        return redirect("/")
                else:
                    messages.error(
                        request, "Invalid username or password. Please try again! ❌"
                    )
            else:
                messages.error(
                    request,
                    "Invalid form submission. Please check the entered data! ❌",
                )
        else:
            form = AuthenticationForm()
        context = {"form": form}
        return render(request, "accounts/login.html", context)
    else:
        return redirect("/")


@login_required
def logout_view(request):
    logout(request)
    messages.success(
        request,
        "You logged out successfully! 🎉",
    )
    return redirect("/")


def signup_view(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.save(commit=False)
                user.is_active = False
                user.save()

                current_site = get_current_site(request)
                mail_subject = "Activation link has been sent to your email id"
                message = render_to_string(
                    "acc_active_email.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    },
                )
                to_email = form.cleaned_data.get("email")
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                messages.warning(
                    request, "We have sent you an email; please confirm 📧"
                )
                return redirect("accounts:login")
            elif not form.is_valid():
                if "username" in form.errors:
                    messages.error(request, "Username already exists! ❌")
                if "email" in form.errors:
                    messages.error(request, "Email already exists! ❌")
                if "password1" in form.errors:
                    messages.error(request, "Password is too weak! ❌")
                if "password2" in form.errors:
                    messages.error(request, "Passwords are not match! ❌")
                if "captcha" in form.errors:
                    messages.error(request, "Invalid Captcha! Please try again! ❌")

        form = RegisterForm()
        context = {"form": form}
        return render(request, "accounts/signup.html", context)
    else:
        return redirect("/")


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        response = HttpResponse(
            "Thank you for your email confirmation. Now you can login to your account."
        )
        response["Refresh"] = f"3;url={reverse('accounts:login')}"
        return response
    else:
        return HttpResponse("Activation link is invalid!")


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = "/accounts/login/"

    def form_valid(self, form):
        uidb64 = self.kwargs["uidb64"]
        token = self.kwargs["token"]
        user = self.get_user(uidb64)

        new_password = form.cleaned_data["new_password1"]

        if user.check_password(new_password):
            messages.error(
                self.request, "New password cannot be the same as the old password! 🚫"
            )
            return self.form_invalid(form)

        user.set_password(new_password)
        user.save()

        messages.success(self.request, "Password reset successful! 🎉")
        return super().form_valid(form)


class CustomPasswordResetView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data.get("email")

        if CustomUser.objects.filter(email=email).exists():
            messages.success(
                self.request,
                "Password reset email has been sent. Please check your inbox. 💌",
            )
        else:
            messages.error(self.request, "User with this email does not exist! 🚫")
            return redirect(reverse_lazy("accounts:password_reset"))

        return super().form_valid(form)


# ! for the MAINTANANCE_MODE
def maintenance(request):
    return render(request, "maintenance.html")
