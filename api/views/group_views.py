from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *


class GroupView(APIView):
    def get(self, request):
        group_list = Group.objects.filter(user=request.user.id, is_confirmed=True)
        data = []
        for group in group_list:
            serializer = GroupSerializer(group)
            user_list = User.objects.filter(group__group_num=group.group_num)
            user_name_list = []
            for user in user_list:
                user_name_list.append(user.name)
            data.append({
                "group_info": serializer.data,
                "user_in_group": user_name_list
            })
        response = {
            "status": status.HTTP_200_OK,
            "data": data
        }
        return Response(response)

    def post(self, request):
        try:
            group_num = Group.objects.latest('group_num').group_num + 1
        except Exception as e:
            print(e)
            group_num = 1
        data = {
            "group_num": group_num,
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
            "group_num": get_object_or_404(Group, id=request.data['id']).group_num,
            "name": get_object_or_404(Group, id=request.data['id']).name,
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
