from datetime import datetime
from operator import itemgetter
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *
from api.mys3client import MyS3Client
from tripfriend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
from face_recognition.face_recognition import face_recognition
from api.permissions import GroupMembersOnly


class PhotoTagView(APIView):
    permission_classes = [GroupMembersOnly]

    def get(self, request, part, trip):
        trip = get_object_or_404(Trip, id=trip)
        self.check_object_permissions(self.request, obj=trip)
        trip_photos = Photo.objects.filter(trip=trip)
        data = []

        if part == 'yolo':
            if trip.yolo_request_num == 0:
                return Response({"아직 객체 분류가 진행되지 않았습니다."}, status.HTTP_200_OK)

            tag_list = trip_photos.values_list('tag_yolo', 'tag_yolo__tag_name')
            for tag in set(tag_list):
                data.append({
                    "tag_id": tag[0],
                    "tag": tag[1],
                    "thumbnail": PhotoReturnSerializer(trip_photos.filter(tag_yolo=tag[0]).last()).data
                })

        elif part == 'face':

            if trip.face_request_num == 0:
                return Response({"아직 인물 분류가 진행되지 않았습니다."}, status.HTTP_200_OK)

            tag_list = trip_photos.values_list('tag_face', 'tag_face__custom_name')
            print(set(tag_list))
            for tag in set(tag_list):
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
        # print(photos)
        # 모델 돌리기 (인자로 url 리스트) -> output: 태그 붙은 딕셔너리
        # part 인자로 어떤 모델 돌릴지 구분
        # Trip의 yolo_request_num, face_request num 증가시키기
        # yolo는 is_sorted_yolo false 인 것에 대해서만 돌리고 돌린 것들은 해당 필드 true로 바꾸기
        # output DB에 저장
        if part == 'yolo':
            return Response(photos)
            # pass
        elif part == 'face':
            result = face_recognition(photos)
            trip.face_request_num = trip.face_request_num + 1
            trip.save()
            # Todo: tag face 리스트 받아서 저장, Photo에 tag face 저장
            tag_id_list = []
            tag_num_list = []
            for image in result[2]:
                sorted_before = get_object_or_404(Photo, id=image['id']).tag_face
                if sorted_before.exists():
                    sorted_before.clear()
            for group_idx in result[1]:
                TagFace.objects.create(tag_num=group_idx)
                tag_id_list.append(TagFace.objects.last().id)
                tag_num_list.append(group_idx)
            for image in result[2]:
                photo = get_object_or_404(Photo, id=image['id'])
                for idx in image['group_idx']:
                    if idx == -2:
                        photo.tag_face.add(1)
                    elif idx == -1:
                        photo.tag_face.add(2)
                    else:
                        photo.tag_face.add(get_object_or_404(TagFace, id=tag_id_list[tag_num_list.index(idx)]))
            # for image in result:
            #     phototagface = PhotoTagFace.objects.filter(photo=image['id'])
            #     if phototagface.exists():
            #         phototagface.delete()
            #     for idx in image['group_idx']:
            #         PhotoTagFace.objects.create(photo=get_object_or_404(Photo, id=image['id']),
            #                                     tagface=get_object_or_404(TagFace, id=(idx + 3)))
        return Response({"사진 자동분류가 완료되었습니다"}, status=status.HTTP_200_OK)


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

