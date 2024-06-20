from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.utils import timezone

from blog.models import Post


def home_view(request):
    posts = Post.objects.filter(published_date__lte=timezone.now(), status=1).order_by(
        "published_date"
    )[:3]

    most_viewed_posts = Post.objects.filter(
        published_date__lte=timezone.now(), status=1
    ).order_by("-counted_views")[:4]

    context = {"posts": posts, "most_viewed_posts": most_viewed_posts}
    return render(request, "website/index.html", context)


def contact_view(request):
    return render(request, "website/contact.html")


def about_view(request):
    return render(request, "website/about.html")
