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
        #날짜별로 묶어서 리턴
        photos = Photo.objects.filter(trip=trip)
        dates = []
        for photo in photos:
            if photo.taken_at is None:
                dates.append(None)
            else:
                dates.append(photo.taken_at.date())

        data = []
        for date in set(dates):
            if date is None:
                data.append({
                    "date": None,
                    "photo": PhotoSerializer(photos.filter(taken_at=None), many=True).data
                })
            else:
                data.append({
                    "date": date,
                    "photo": PhotoSerializer(photos.filter(taken_at__day=date.day), many=True).data
                })
        response = {
            "status": status.HTTP_200_OK,
            "data": data
        }
        return Response(response)

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
            "taken_at": taken_at,
            "uploaded_by": request.user.id
        }

        serializer = PhotoSerializer(data=data)
        img.close()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PhotoCategoryView(APIView):
    def get(self, request, trip, category):
        if category is 'scene':
            pass  #아직 안한거
        else:
            photos = Photo.objects.filter(trip=trip, category_cv=category)
            serializer = PhotoSerializer(photos, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
