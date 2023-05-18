from .base import *

# DEBUG = env('DEBUG')
DEBUG = True

ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env('DATABASE_NAME'),
        'USER': env('DATABASE_USER'),
        'PASSWORD': env('DATABASE_PASSWORD'),
        'HOST': env('DATABASE_HOST'),
        'PORT': env('DATABASE_PORT'),
    }
}

CELERY_BROKER_URL = 'redis://redis-server:6379/0'
CELERY_RESULT_BACKEND = 'redis://redis-server:6379/0'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Seoul'
