from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from photos.serializers import *
from base.permissions import GroupMembersOnly
from photos.requests import flask_post_request
from trips.models import *


class PhotoYoloView(APIView):
    permission_classes = [GroupMembersOnly]

    def get(self, request, trip):
        trip = get_object_or_404(Trip, id=trip)
        self.check_object_permissions(self.request, obj=trip)
        trip_photos = Photo.objects.filter(trip=trip, deleted_at=None)
        data = []

        tag_list = trip_photos.values_list('tag_yolo', 'tag_yolo__tag_name_kr')
        for tag in set(tag_list):
            if tag[0] is None:
                continue
            data.append({
                "tag_id": tag[0],
                "tag": tag[1],
                "thumbnail": PhotoReturnSerializer(trip_photos.filter(tag_yolo=tag[0]).last()).data
            })

        response = {
            "status": status.HTTP_200_OK,
            "data": data
        }
        return Response(response)

    def post(self, request, trip):
        trip = get_object_or_404(Trip, id=trip)
        self.check_object_permissions(self.request, obj=trip)
        photos = Photo.objects.filter(trip=trip, is_sorted_yolo=False, deleted_at=None).values('id', 'url')

        result = flask_post_request(endpoint="yolo", images=photos)
        if result.status_code == 200:
            for image in result.json():
                photo = get_object_or_404(Photo, id=image['id'])
                for tag in image['yolo_tag']:
                    photo.tag_yolo.add(get_object_or_404(TagYolo, tag_name=tag))
                photo.is_sorted_yolo = True
                photo.save()
            return Response({"사진 자동분류가 완료되었습니다"}, status=status.HTTP_200_OK)
        return result


class PhotoYoloDetailView(APIView):
    permission_classes = [GroupMembersOnly]

    def get(self, request, trip, tag):
        self.check_object_permissions(self.request, obj=get_object_or_404(Trip, id=trip))
        photos = Photo.objects.filter(trip=trip, tag_yolo=tag, deleted_at=None)
        data = {
            "tag": get_object_or_404(TagYolo, id=tag).tag_name_kr,
            "photos": PhotoReturnSerializer(photos, many=True).data
        }
        return Response(data, status.HTTP_200_OK)
