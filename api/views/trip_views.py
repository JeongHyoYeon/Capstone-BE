from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *
from .group_views import GroupView
import boto3
import uuid
from tripfriend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME

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
        except:
            return None


class PersonalTripView(APIView):
    def get(self, request):
        trip_list = Trip.objects.filter(group__user=request.user.id)
        serializer = TripSerializer(trip_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GroupTripView(APIView):
    def get(self, request):
        group_list = GroupView.get()
        trip_list = Trip.objects.filter(group__in=group_list)
        serializer = TripSerializer(trip_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        s3_client = MyS3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)



