from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from accounts.models import CustomUser

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(SummernoteModelAdmin):
    empty_value_display = "-empty-"
    list_display = ["username", "first_name", "email"]
