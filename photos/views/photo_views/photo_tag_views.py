from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.serializers import *
from photos.permissions import GroupMembersOnly
from photos.request import flask_post_request

class PhotoTagView(APIView):
    permission_classes = [GroupMembersOnly]

    def get(self, request, part, trip):
        trip = get_object_or_404(Trip, id=trip)
        self.check_object_permissions(self.request, obj=trip)
        trip_photos = Photo.objects.filter(trip=trip)
        data = []

        if part == 'yolo':
            tag_list = trip_photos.values_list('tag_yolo', 'tag_yolo__tag_name_kr')
            for tag in set(tag_list):
                if tag[0] is None:
                    continue
                data.append({
                    "tag_id": tag[0],
                    "tag": tag[1],
                    "thumbnail": PhotoReturnSerializer(trip_photos.filter(tag_yolo=tag[0]).last()).data
                })

        elif part == 'face':
            tag_list = trip_photos.values_list('tag_face', 'tag_face__custom_name')
            print(set(tag_list))
            for tag in set(tag_list):
                if tag[0] is None:
                    continue
                data.append({
                    "tag_id": tag[0],
                    "tag": tag[1],
                    "thumbnail": PhotoReturnSerializer(trip_photos.filter(tag_face=tag[0]).last()).data
                })

        elif part == 'uploader':
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

    def post(self, request, part, trip):
        trip = get_object_or_404(Trip, id=trip)
        self.check_object_permissions(self.request, obj=trip)
        photos = Photo.objects.filter(trip=trip).values('id', 'url')

        if part == 'yolo':
            photos = photos.filter(is_sorted_yolo=False)

        result = flask_post_request(endpoint=part, images=photos)
        if result.status_code == 200:
            if part == 'yolo':
                for image in result.json():
                    photo = get_object_or_404(Photo, id=image['id'])
                    for tag in image['yolo_tag']:
                        photo.tag_yolo.add(get_object_or_404(TagYolo, tag_name=tag))
                    photo.is_sorted_yolo = True
                    photo.save()

            elif part == 'face':
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


class PhotoTagDetailView(APIView):
    permission_classes = [GroupMembersOnly]

    def get(self, request, part, trip, tag):
        self.check_object_permissions(self.request, obj=get_object_or_404(Trip, id=trip))
        if part == 'yolo':
            photos = Photo.objects.filter(trip=trip, tag_yolo__photos=tag)
        elif part == 'face':
            photos = Photo.objects.filter(trip=trip, tag_face__photos=tag)
        serializer = PhotoReturnSerializer(photos, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    # def post(self, request, part, trip, tag):
    #     # 파일 다운로드
    #     if part == 'yolo':
    #         photos = Photo.objects.filter(trip=trip, tag_yolo__photos=tag)
    #     elif part == 'face':
    #         photos = Photo.objects.filter(trip=trip, tag_face__photos=tag)
    #     elif part == 'uploader':
    #         photos = Photo.objects.filter(trip=trip, uploaded_by=tag)
    #     s3_client = MyS3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)
    #     for photo in photos:
    #         s3_client.download(photo)
    #     return Response({"다운로드가 완료되었습니다."}, status.HTTP_200_OK)


class PhotoUploaderDetailView(APIView):
    permission_classes = [GroupMembersOnly]

    def get(self, request, trip, user):
        self.check_object_permissions(self.request, obj=get_object_or_404(Trip, id=trip))
        photos = Photo.objects.filter(trip=trip, uploaded_by=user)
        serializer = PhotoReturnSerializer(photos, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

