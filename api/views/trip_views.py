from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *
from .group_views import GroupView


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
