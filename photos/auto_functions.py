from photos.mys3client import MyS3Client
from tripfriend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
from .models import *
from datetime import timedelta
from django.utils.timezone import now

class DeletePhotos:
    photos = Photo.objects.filter(created_at__lt=now() - timedelta(days=14))
    s3_client = MyS3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)

    def s3_delete(self):
        for photo in self.photos:
            self.s3_client.delete(photo)

    def db_delete(self):
        self.photos.delete()  # hard delete


