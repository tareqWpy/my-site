from django.urls import path

from .views import *

app_name = "website"

urlpatterns = [
    path("", home_view, name="home"),
    path("contact", contact_view, name="contact"),
    path("about", about_view, name="about"),
]
