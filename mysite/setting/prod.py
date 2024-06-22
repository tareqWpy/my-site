import os
from email.policy import default

from decouple import config

from mysite.settings import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", cast=bool, default=False)

# SECURITY WARNING: don't run with debug turned on in production!

MAINTANANCE_MODE = int(os.environ.get("MAINTANANCE_MODE", 0))

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # Add this
    "compressor.finders.CompressorFinder",
)

COMPRESS_CSS_HASHING_METHOD = "content"
COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.rCSSMinFilter",
    ],
    "js": [
        "compressor.filters.jsmin.JSMinFilter",
    ],
}
HTML_MINIFY = True
KEEP_COMMENTS_ON_MINIFYING = True

COMPRESS_ENABLED = True


ALLOWED_HOSTS = ["djangotech.online", "www.djangotech.online"]
# ALLOWED_HOSTS = ["*"]


# ? site framework
SITE_ID = 2

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": config("DB_ENGINE"),
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

# ! this for python manage.py collecstatic
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# security configs for production
if config("USE_SSL_SETTING", cast=bool, default=False):
    # Https settings
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_PRELOAD = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    # more security settings
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "SAMEORIGIN"
    SECURE_REFERRER_POLICY = "strict-origin"
    USE_X_FORWARDED_HOST = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
