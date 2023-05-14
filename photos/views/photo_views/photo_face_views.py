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

    def post(self, request, trip):
        trip = get_object_or_404(Trip, id=trip)
        self.check_object_permissions(self.request, obj=trip)
        photos = Photo.objects.filter(trip=trip).values('id', 'url')

        result = flask_post_request(endpoint="face", images=photos)
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

    def get(self, request, trip, tag):
        self.check_object_permissions(self.request, obj=get_object_or_404(Trip, id=trip))
        photos = Photo.objects.filter(trip=trip, tag_face=tag)
        data = {
            "tag": get_object_or_404(TagFace, id=tag).custom_name,
            "photos": PhotoReturnSerializer(photos, many=True).data
        }
        return Response(data, status.HTTP_200_OK)

    def patch(self, request, trip, tag):
        self.check_object_permissions(self.request, obj=get_object_or_404(Trip, id=trip))
        tagface = get_object_or_404(TagFace, id=tag)
        serializer = TagFaceSerializer(tagface, {'custom_name': request.data['custom_name']}, partial=True)  # 다른거 바뀌면 안돼서..
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)