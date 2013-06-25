import dj_database_url

from source.settings.defaults import *


DEBUG = False
LOCAL_SERVE = False

# Databases
DATABASES = {'default': dj_database_url.config()}
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Caching
CACHES = None

# Only cache for users who aren't logged in
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# Paths
PUBLIC_ROOT = get_path(PROJECT_ROOT, '../public/')
MEDIA_ROOT = get_path(PUBLIC_ROOT, 'media/')
STATIC_ROOT = get_path(PUBLIC_ROOT, 'static/')

# Email
EMAIL_HOST = None
EMAIL_HOST_USER = None
EMAIL_HOST_PASSWORD = None
EMAIL_PORT = 25
EMAIL_USE_TLS = False
