# SECURITY WARNING: keep the secret key used in production secret!
from decouple import config

from mysite.settings import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/


SECRET_KEY = config("SECRET_KEY")
DEBUG = True

ALLOWED_HOSTS = ["*"]


# ? site framework
SITE_ID = 2

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ! this for python manage.py collecstatic
STATIC_ROOT = BASE_DIR / "staticfiles/"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
