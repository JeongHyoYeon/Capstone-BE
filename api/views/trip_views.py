from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *
from api.mys3client import MyS3Client
from tripfriend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
import json
from api.permissions import GroupMembersOnly

class PersonalTripView(APIView):
    def get(self, request):
        group_list = Group.objects.filter(usergroup__user_id=request.user.id, usergroup__is_confirmed=True)
        trip_list = Trip.objects.filter(group__in=group_list)
        data = []
        for trip in trip_list:
            data.append({
                "group": get_object_or_404(Group, id=trip.group).name,
                "trip_info": TripSerializer(trip).data
            })
        response = {
            "status": status.HTTP_200_OK,
            "data": data
        }
        return Response(response)


class GroupTripView(APIView):
    permission_classes = [GroupMembersOnly]

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
            thumbnail = s3_client.upload(request.FILES['thumbnail'])[1]
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
    permission_classes = [GroupMembersOnly]

    def get(self, request, trip):
        trip = get_object_or_404(Trip, id=trip)
        self.check_object_permissions(self.request, obj=trip)
        serializer = TripSerializer(trip)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, trip):
        trip_instance = get_object_or_404(Trip, id=trip)
        self.check_object_permissions(self.request, obj=trip_instance)
        serializer = TripSerializer(instance=trip_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




