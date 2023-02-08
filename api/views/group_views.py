from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *

class NewGroupView(APIView):
    def post(self, request):
        data = {
            "name": request.data.get("name"),
            "user": request.user.id,
            "is_confirmed": True
        }
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupView(APIView):
    def post(self, request):
        data = {
            "name": get_object_or_404(Group, user=request.user.id).name,
            "user": request.data['invited_user'],
            "is_confirmed": False
        }
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        group_instance = get_object_or_404(Group, user=request.user.id)
        serializer = GroupSerializer(instance=group_instance, data={"is_confirmed": True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)