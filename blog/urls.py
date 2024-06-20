from django.urls import path

from blog.feeds import LatestEntriesFeed

from .views import *

app_name = "blog"

urlpatterns = [
    path("", post_list_view, name="post-list"),
    path("category/<str:cat_name>/", post_list_view, name="post-category"),
    path("tags/<str:tag_name>/", post_list_view, name="post-tags"),
    path("author/<str:author_username>/", post_list_view, name="post-author"),
    path("search/", post_search_view, name="post-search"),
    path("post-single/<int:pid>/", post_single_view, name="post-single"),
    path("rss/feed/", LatestEntriesFeed()),
]
