from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from photos.serializers import *
from photos.permissions import GroupMembersOnly
from trips.models import *
from accounts.models import User


class PhotoUploaderView(APIView):
    permission_classes = [GroupMembersOnly]

    def get(self, request, trip):
        trip = get_object_or_404(Trip, id=trip)
        self.check_object_permissions(self.request, obj=trip)
        trip_photos = Photo.objects.filter(trip=trip)
        data = []

        tag_list = trip_photos.values_list('uploaded_by', 'uploaded_by__name')
        for tag in set(tag_list):
            data.append({
                "tag_id": tag[0],
                "tag": tag[1],
                "thumbnail": PhotoReturnSerializer(trip_photos.filter(uploaded_by=tag[0]).last()).data
            })

        response = {
            "status": status.HTTP_200_OK,
            "data": data
        }
        return Response(response)


class PhotoUploaderDetailView(APIView):
    permission_classes = [GroupMembersOnly]

    def get(self, request, trip, user):
        self.check_object_permissions(self.request, obj=get_object_or_404(Trip, id=trip))
        photos = Photo.objects.filter(trip=trip, uploaded_by=user)
        data = {
            "tag": get_object_or_404(User, id=user).name,
            "photos": PhotoReturnSerializer(photos, many=True).data
        }
        return Response(data, status.HTTP_200_OK)

