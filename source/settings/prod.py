from .defaults import *
from .secrets import *


DEBUG = False
LOCAL_SERVE = False

# Databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'PORT': 5433,
        'NAME': 'bbox_pong',
        'USER': 'postgres',
        'PASSWORD': DATABASE_PASSWORD,
    },
}

# Caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 300,
        'KEY_PREFIX': 'pong',
    },
}

# Only cache for users who aren't logged in
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'
