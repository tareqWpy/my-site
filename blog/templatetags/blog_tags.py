from django import template
from django.utils import timezone

from blog.models import Category, Post

register = template.Library()


@register.inclusion_tag("blog/blog-latest-posts.html")
def latest_post():
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now()).order_by(
        "-published_date"
    )[:4]
    return {"posts": posts}


@register.inclusion_tag("blog/blog-post-categories.html")
def post_category():
    posts = Post.objects.filter(status=1, published_date__lte=timezone.now()).order_by(
        "-published_date"
    )
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name] = posts.filter(category=name).count()

    return {"categories": cat_dict}
