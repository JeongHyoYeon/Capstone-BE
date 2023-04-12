from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *
from api.mys3client import MyS3Client
from tripfriend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME


class PhotoTagView(APIView):
    def get(self, request, part, trip):
        # TODO: 카테고리 리스트 & 썸네일 리턴
        if part == 'yolo':
            pass
        if part == 'face':
            pass

    def patch(self, request, part, trip):
        photos = Photo.objects.filter(trip=trip).values('id', 'url')
        print(photos)
        trip_object = get_object_or_404(Trip, id=trip)
        # 모델 돌리기 (인자로 url 리스트) -> output: 태그 붙은 딕셔너리
        # part 인자로 어떤 모델 돌릴지 구분
        # output DB에 저장(수정)
        return Response({"사진 자동 분류가 완료되었습니다."}, status.HTTP_200_OK)


class PhotoTagDetailView(APIView):
    def get(self, request, part, trip, tag):
        if part == 'yolo':
            photos = Photo.objects.filter(trip=trip, tag_yolo__photos=tag)
            print(photos)
            serializer = PhotoReturnSerializer(photos, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        if part == 'face':
            photos = Photo.objects.filter(trip=trip, tag_face__photos=tag)
            serializer = PhotoReturnSerializer(photos, many=True)
            return Response(serializer.data, status.HTTP_200_OK)


    def post(self, request, part, trip, tag):
        # 파일 다운로드
        # TODO: 폴더 안에 있는 사진만 다운로드 받게 수정
        photos = Photo.objects.filter(trip=trip)  # 다운로드 테스트용
        s3_client = MyS3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)
        for photo in photos:
            s3_client.download(photo)
        return Response({"다운로드가 완료되었습니다."}, status.HTTP_200_OK)