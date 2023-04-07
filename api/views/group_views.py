from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *


class GroupView(APIView):
    def get(self, request):
        user_groups = UserGroup.objects.filter(user=request.user.id, is_confirmed=True)
        data = []
        for user_group in user_groups:
            group = get_object_or_404(Group, id=user_group.group.id)
            user_list = User.objects.filter(usergroup__group=group.id, usergroup__is_confirmed=True)
            user_name_list = []
            for user in user_list:
                user_name_list.append(user.name)
            data.append({
                "group_info": GroupSerializer(group).data,
                "user_in_group": user_name_list
            })
        response = {
            "status": status.HTTP_200_OK,
            "data": data
        }
        return Response(response)

    def post(self, request):
        data1 = {
            "name": request.data.get("name")
        }
        serializer1 = GroupSerializer(data=data1)
        if serializer1.is_valid():
            group = serializer1.save()
            data2 = {
                "user": request.user.id,
                "group": group.id,
                "is_confirmed": True
            }
            serializer2 = UserGroupSerializer(data=data2)
            if serializer2.is_valid():
                serializer2.save()
                serializer_data = [serializer1.data, serializer2.data]
                return Response(serializer_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer2.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupInviteView(APIView):
    def post(self, request):
        data = {
            "group": request.data['group'],
            "user": request.data['user'],
            "is_confirmed": False
        }
        serializer = UserGroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        invites = UserGroup.objects.filter(user=request.user.id, is_confirmed=False)
        data = []
        for invite in invites:
            data.append({
                "user_group": UserGroupSerializer(invite).data,
                "group_name": invite.group.name
            })
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        user_group_instance = get_object_or_404(UserGroup, id=request.data['user_group_id'])
        serializer = UserGroupSerializer(instance=user_group_instance, data={"is_confirmed": True}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
