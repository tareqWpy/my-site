from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.utils import timezone

from blog.models import Post


def home_view(request):
    posts = Post.objects.filter(published_date__lte=timezone.now(), status=1).order_by(
        "published_date"
    )[:3]

    context = {"posts": posts}
    return render(request, "website/index.html", context)


def contact_view(request):
    return render(request, "website/contact.html")


def about_view(request):
    return render(request, "website/about.html")
