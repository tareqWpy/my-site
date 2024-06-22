import random

from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils import timezone

from blog.models import Post
from website.forms import ContactForm, NewsletterForm
from website.models import Newsletter


def home_view(request):
    posts = Post.objects.filter(published_date__lte=timezone.now(), status=1).order_by(
        "published_date"
    )[:3]

    all_posts = Post.objects.filter(published_date__lte=timezone.now(), status=1)

    random_posts = random.sample(list(all_posts), 4)

    most_viewed_posts = Post.objects.filter(
        published_date__lte=timezone.now(), status=1
    ).order_by("-counted_views")[:4]

    context = {
        "posts": posts,
        "most_viewed_posts": most_viewed_posts,
        "random_posts": random_posts,
    }
    return render(request, "website/index.html", context)


def about_view(request):
    return render(request, "website/about.html")


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your contact has been created successfully! 🎉")
        else:
            messages.error(
                request, "Failed to create a contact. Please check your input. 🚫"
            )
    else:
        form = ContactForm()
    return render(request, "website/contact.html", {"form": form})


def newsletter_view(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your email submitted successfully! 💌")
            return redirect("/")
        elif not form.is_valid():
            email = form.data.get("email")
            if Newsletter.objects.filter(email=email).exists():
                messages.error(request, "This email is already subscribed! 🚫")
            else:
                messages.error(
                    request,
                    "There was an error submitting your email. Please try again. 😕",
                )
                return redirect("/")

    # Handle GET request
    return redirect("/")


def error_400(request, exception):
    return render(request, "errors/handler400.html")


def error_403(request, exception):
    return render(request, "errors/handler403.html")


def error_404(request, exception):
    return render(request, "errors/handler404.html")


def error_500(request):
    return render(request, "errors/handler500.html")
