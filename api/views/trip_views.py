from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *
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
    def get(self, request, group):
        trip_list = Trip.objects.filter(group=group)
        serializer = TripSerializer(trip_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, group):
        s3_client = MyS3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)
        data = {
            "group": group,
            "place": request.data.get("place"),
            "departing_date": request.data.get("departing_date"),
            "arriving_date": request.data.get("arriving_date"),
            "thumbnail": s3_client.upload(request.FILES)
        }
        serializer = TripSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



