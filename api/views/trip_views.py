from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *
import boto3
import uuid
from tripfriend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
import json

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


class PersonalTripView(APIView):
    def get(self, request):
        group_list = Group.objects.filter(user=request.user.id)
        trip_list = Trip.objects.filter(group__in=group_list.values_list('group_num'))
        data = []
        for trip in trip_list:
            group_name = Group.objects.filter(group_num=trip.group)[0].name
            data.append({
                "group": group_name,
                "trip_info": TripSerializer(trip).data
            })
        response = {
            "status": status.HTTP_200_OK,
            "data": data
        }
        return Response(response)


class GroupTripView(APIView):
    def get(self, request, group):
        trip_list = Trip.objects.filter(group=group)
        serializer = TripSerializer(trip_list, many=True)
        response = {
            "status": status.HTTP_200_OK,
            "data": {
                "group_name": get_object_or_404(Group, id=group).name,
                "trip_list": serializer.data
            }
        }
        return Response(response)

    def post(self, request, group):
        s3_client = MyS3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)
        try:
            thumbnail = s3_client.upload(request.FILES['thumbnail'])
        except Exception as e:
            print(e)
            thumbnail = None
        data = {
            "group": group,
            "place": json.loads(request.data.get("place")),
            "departing_date": json.loads(request.data.get("departing_date")),
            "arriving_date": json.loads(request.data.get("arriving_date")),
            "thumbnail": thumbnail
        }
        serializer = TripSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TripDetailView(APIView):
    def get(self, request, trip):
        trip = get_object_or_404(Trip, id=trip)
        serializer = TripSerializer(trip)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, trip):
        trip_instance = get_object_or_404(Trip, id=trip)
        serializer = TripSerializer(instance=trip_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




