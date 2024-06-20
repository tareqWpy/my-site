from django.contrib import messages
from django.shortcuts import redirect, render


def home_view(request):
    return render(request, "website/index.html")
