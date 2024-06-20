from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils import timezone

from blog.models import Post


class LatestEntriesFeed(Feed):
    title = "Blog newest posts"
    link = "/rss/feed"
    description = "my blog"

    def items(self):
        return Post.objects.filter(
            published_date__lte=timezone.now(), status=1
        ).order_by("-published_date")

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content
