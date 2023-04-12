from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *
from api.mys3client import MyS3Client
from tripfriend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME


class PhotoTagView(APIView):
    def patch(self, request, part, trip):
        photos = Photo.objects.filter(trip=trip).values_list('id', 'url')
        print(photos)
        trip_object = get_object_or_404(Trip, id=trip)
        # 모델 돌리기 (인자로 url 리스트) -> output: 태그 붙은 딕셔너리
        # output DB에 저장(수정)
        return Response({"사진 자동 분류가 완료되었습니다."}, status.HTTP_200_OK)


class PhotoTagDetailView(APIView):
    def get(self, request, part, trip, tag):
        # Todo: tag 정보 검색 수정해야 - Yolo 부분 확정되면 고칠 예정
        if tag == 'scene':
            # 풍경 안에 있는 카테고리 리스트 리턴
            # 다시 선택할 경우 이 api 다시 요청
            photos = Photo.objects.filter(trip=trip)
            scene_classes = ['buildings', 'forests', 'glacier', 'mountains', 'sea', 'street']
            data = []
            for scene in scene_classes:
                if scene in photos.values_list('tag_yolo__tag_name'):
                    data.append(
                        {
                            "tag": scene,
                            "thumbnail": Photo.objects.filter(trip=trip, tag_yolo__tag_name=scene)[0]
                        }
                    )
            response = {
                "status": status.HTTP_200_OK,
                "data": data
            }
            return Response(response)

        else:
            photos = Photo.objects.filter(trip=trip, tag_yolo__tag_name=tag)
            serializer = PhotoReturnSerializer(photos, many=True)
            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request, part, trip, tag):
        # 파일 다운로드
        # trip_photos = Photo.objects.filter(trip=trip)
        # tag_yolo_list = trip_photos.values_list('tag_yolo__tag_name', flat=True)
        # # tag_face_list = trip_photos.values_list('tag_face__tag_num', flat=True)
        # photos = trip_photos.filter(tag__in=tag_yolo_list)
        photos = Photo.objects.filter(trip=trip)  # 다운로드 테스트용
        s3_client = MyS3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)
        for photo in photos:
            s3_client.download(photo)
        return Response({"다운로드가 완료되었습니다."}, status.HTTP_200_OK)