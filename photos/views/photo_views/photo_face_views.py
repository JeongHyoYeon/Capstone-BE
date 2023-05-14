from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from photos.serializers import *
from photos.permissions import GroupMembersOnly
from photos.request import flask_post_request
from trips.models import *


class PhotoFaceView(APIView):
    permission_classes = [GroupMembersOnly]

    def get(self, request, trip):
        trip = get_object_or_404(Trip, id=trip)
        self.check_object_permissions(self.request, obj=trip)
        trip_photos = Photo.objects.filter(trip=trip)
        data = []

        tag_list = Photo.objects.filter(trip=trip).values_list('tag_face', 'tag_face__custom_name')
        for tag in set(tag_list):
            if tag[0] is None:
                continue
            data.append({
                "tag_id": tag[0],
                "tag": tag[1],
                "thumbnail": PhotoReturnSerializer(trip_photos.filter(tag_face=tag[0]).last()).data
            })

        response = {
            "status": status.HTTP_200_OK,
            "data": data
        }
        return Response(response)

    def post(self, request, part, trip):
        trip = get_object_or_404(Trip, id=trip)
        self.check_object_permissions(self.request, obj=trip)
        photos = Photo.objects.filter(trip=trip).values('id', 'url')

        result = flask_post_request(endpoint=part, images=photos)
        if result.status_code == 200:
            tag_id_list = []
            tag_num_list = []
            result = result.json()
            for image in result['images']:
                sorted_before = get_object_or_404(Photo, id=image['id']).tag_face
                if sorted_before.exists():
                    sorted_before.clear()
            for group_idx in result['group_idx_list']:
                TagFace.objects.create(tag_num=group_idx)
                tag_id_list.append(TagFace.objects.last().id)
                tag_num_list.append(group_idx)
            for image in result['images']:
                photo = get_object_or_404(Photo, id=image['id'])
                for idx in image['group_idx']:
                    if idx == -2:
                        photo.tag_face.add(1)
                    elif idx == -1:
                        photo.tag_face.add(2)
                    else:
                        photo.tag_face.add(get_object_or_404(TagFace, id=tag_id_list[tag_num_list.index(idx)]))
            return Response({"사진 자동분류가 완료되었습니다"}, status=status.HTTP_200_OK)
        return result


class PhotoFaceDetailView(APIView):
    permission_classes = [GroupMembersOnly]

    def get(self, request, part, trip, tag):
        self.check_object_permissions(self.request, obj=get_object_or_404(Trip, id=trip))
        photos = Photo.objects.filter(trip=trip, tag_face__photos=tag)
        serializer = PhotoReturnSerializer(photos, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
