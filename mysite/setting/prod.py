from mysite.settings import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-6wd1ilp$u+0=9q7ndw_azwtl_5s1(0cqfzhsw-szr-oc!u8ycj"

# SECURITY WARNING: don't run with debug turned on in production!
# ! DEBUG should be false in production
DEBUG = True

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


# ALLOWED_HOSTS = ["djangotech.online", "www.djangotech.online"]
ALLOWED_HOSTS = ["*"]


# ? site framework
SITE_ID = 2

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
"""
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "mysite_mysql",
        "USER": "root",
        "PASSSWORD": "S^AQ#7P36",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
"""

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ! this for python manage.py collecstatic
STATIC_ROOT = BASE_DIR / "statics"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

CSRF_COOKIE_SECURE = True
