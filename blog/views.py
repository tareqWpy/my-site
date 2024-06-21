from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from blog.forms import CommentForm
from blog.models import Comment, Post


def post_list_view(request, **kwargs):
    posts = Post.objects.filter(published_date__lte=timezone.now(), status=1)
    if kwargs.get("cat_name") is not None:
        posts = posts.filter(category__category_name=kwargs["cat_name"])
    if kwargs.get("author_username") is not None:
        posts = posts.filter(author__username=kwargs["author_username"])
    if kwargs.get("tag_name") is not None:
        posts = posts.filter(tags__name__in=[kwargs["tag_name"]])

    posts = Paginator(list(posts), 4)

    try:
        page_number = request.GET.get("page")
        posts = posts.get_page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)

    most_viewed_posts = Post.objects.filter(
        published_date__lte=timezone.now(), status=1
    ).order_by("-counted_views")[:3]

    context = {
        "posts": posts,
        "most_viewed_posts": most_viewed_posts,
    }
    return render(request, "blog/post-list.html", context)


def post_search_view(request):
    posts = Post.objects.filter(published_date__lte=timezone.now(), status=1)
    if request.method == "GET":
        search = request.GET.get("s")
        if search:
            search = search.lower()
            posts = posts.filter(
                Q(content__contains=search)
                | Q(author__username__contains=search)
                | Q(title__contains=search)
                | Q(category__category_name__contains=search)
                | Q(tags__name__contains=search)
            ).distinct()
    context = {"posts": posts}
    return render(request, "blog/post-list.html", context)


def counted_view(request, post):
    post.counted_views += 1
    post.save()
    context = {"post": post}
    return render(request, "blog/post-single.html", context)


@login_required
def post_single_view(request, pid):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Your comment submited! But it needs to be approved by admin. 🚫",
            )
        else:
            messages.error(request, "Failed to submit your comment! 🚫")

    post = get_object_or_404(Post, pk=pid, published_date__lte=timezone.now(), status=1)
    # Query for the next post
    next_post = (
        Post.objects.filter(
            published_date__gt=post.published_date,
            status=1,
            published_date__lte=timezone.now(),
        )
        .order_by("published_date")
        .first()
    )

    # Query for the previous post
    prev_post = (
        Post.objects.filter(
            published_date__lt=post.published_date,
            status=1,
            published_date__lte=timezone.now(),
        )
        .order_by("-published_date")
        .first()
    )

    if not post.login_required:
        comments = Comment.objects.filter(post=post.id, approved=True).order_by(
            "-created_date"
        )
        form = CommentForm()
        context = {
            "comment_form": form,
            "comments": comments,
            "author": post.author,
            "current_post": post,
            "prev_post": prev_post,
            "next_post": next_post,
        }
        counted_view(request, post)
        return render(request, "blog/post-single.html", context)
    # else:
    #     return redirect("accounts:login")


# def error_400(request, exception):
#     return render(request, "error/handler400.html")


# def error_403(request, exception):
#     return render(request, "error/handler403.html")


# def error_404(request, exception):
#     return render(request, "error/handler404.html")


# def error_500(request):
#     return render(request, "error/handler500.html")
