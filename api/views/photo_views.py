from datetime import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *
import boto3
import uuid
from tripfriend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
from PIL import Image
from PIL.ExifTags import TAGS

class MyS3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        boto3_s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        self.s3_client = boto3_s3
        self.bucket_name = bucket_name

    def upload(self, file):
        try:
            file_id = str(uuid.uuid4())
            extra_args = {'ContentType': file.content_type}

            self.s3_client.upload_fileobj(
                    file,
                    self.bucket_name,
                    file_id,
                    ExtraArgs=extra_args
                )
            return f'https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_id}'
        except Exception as e:
            print(e)
            return None


class PhotoView(APIView):
    def get(self, request, trip):
        photos = Photo.objects.filter(trip=trip)
        serializer = PhotoSerializer(photos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, trip):
        photo = request.FILES['photo']
        taken_at = None
        img = Image.open(photo)
        img_info = img._getexif()
        for tag_id in img_info:
            tag = TAGS.get(tag_id, tag_id)
            img_data = img_info.get(tag_id)
            if tag == 'DateTimeOriginal':
                taken_at = datetime.strptime(img_data, '%Y:%m:%d %H:%M:%S')
                print(taken_at)

        s3_client = MyS3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)
        url = s3_client.upload(photo)

        data = {
            "trip": trip,
            "url": url,
            "taken_at": taken_at
        }

        serializer = PhotoSerializer(data=data)
        img.close()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)