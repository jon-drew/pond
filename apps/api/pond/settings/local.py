from .base import *

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Relax cookie security in local dev
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
