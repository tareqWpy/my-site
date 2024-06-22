from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from blog.models import Category, Comment, Post

# Register your models here.


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    date_hierarchy = "published_date"
    empty_value_display = "-empty-"
    list_display = (
        "title",
        "author",
        "counted_views",
        "status",
        "login_required",
        "published_date",
        "image",
    )
    list_filter = ("status", "author")
    ordering = ["created_date"]
    search_fields = ("title",)

    # * for summernote fields
    summernote_fields = ("content",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = ("name", "subject", "approved", "created_date")
    list_filter = ("name", "approved")
    ordering = ["created_date"]
    search_fields = ("subject",)


# admin.site.register(Post)
admin.site.register(Category)
