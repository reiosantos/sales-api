from api.settings import *

ALLOWED_HOSTS = ['*']

DEBUG = True

SSL_ENABLED = False

INSTALLED_APPS += [
	'silk',
]

MIDDLEWARE = ['silk.middleware.SilkyMiddleware'] + MIDDLEWARE

SILKY_META = True
SILKY_PYTHON_PROFILER = True

SILKY_DYNAMIC_PROFILING = []

# disable ssl
DATABASES['default']['OPTIONS'].pop('sslmode')
