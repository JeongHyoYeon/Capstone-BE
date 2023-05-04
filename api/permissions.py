from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from django.shortcuts import get_object_or_404
from api.models import *


class GroupMembersOnly(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):  # trip object 전달
        if request.user.is_authenticated:
            user_groups = Group.objects.filter(usergroup__user_id=request.user.id, usergroup__is_confirmed=True)
            trip_group = get_object_or_404(Group, id=obj.group)
            if trip_group in user_groups:
                return True
            raise PermissionDenied()
        raise NotAuthenticated()
