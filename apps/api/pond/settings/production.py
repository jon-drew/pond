from .base import *
import dj_database_url
from decouple import config, Csv

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}
DATABASES['default']['CONN_HEALTH_CHECKS'] = True

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='', cast=Csv())

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
