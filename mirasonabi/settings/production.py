from .base import *
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
CSRF_TRUSTED_ORIGINS = ['https://kanoonmns.ir']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
