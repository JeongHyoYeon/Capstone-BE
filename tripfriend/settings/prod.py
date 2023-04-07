from .base import *

DEBUG = True
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS')

ACCOUNT_DEFAULT_HTTP_PROTOCOL='https'

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

AWS_ACCESS_KEY_ID = 'Access key ID 입력' # .csv 파일에 있는 내용을 입력 Access key ID
AWS_SECRET_ACCESS_KEY = 'Secret acess Key 입력' # .csv 파일에 있는 내용을 입력 Secret access key
AWS_REGION = 'ap-northeast-2'

AWS_STORAGE_BUCKET_NAME = 'lee-teset-bucket' # 설정한 버킷 이름
AWS_S3_CUSTOM_DOMAIN = '%s.s3.%s.amazonaws.com' % (AWS_STORAGE_BUCKET_NAME,AWS_REGION)
AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}
