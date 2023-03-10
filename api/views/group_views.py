from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *


class GroupView(APIView):
    def get(self, request):
        group_list = Group.objects.filter(user=request.user.id, is_confirmed=True)
        serializer = GroupSerializer(group_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


class GroupInviteView(APIView):
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

    def get(self, request):
        invites = Group.objects.filter(user=request.user.id, is_confirmed=False)
        serializer = GroupSerializer(invites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        group_instance = get_object_or_404(Group, id=request.data['group_id'])
        serializer = GroupSerializer(instance=group_instance, data={"is_confirmed": True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
