from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *
import boto3
import uuid
from tripfriend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
from PIL import Image
from PIL.ExifTags import TAGS


class MyS3Client:
    def __init__(self, access_key, secret_key, bucket_name):
        boto3_s3 = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )
        self.s3_client = boto3_s3
        self.bucket_name = bucket_name

    def upload(self, file):
        try:
            file_id = str(uuid.uuid4())
            file_name = file.name
            extra_args = {'ContentType': file.content_type}

            self.s3_client.upload_fileobj(
                    file,
                    self.bucket_name,  # bucket
                    file_id,  # key
                    ExtraArgs=extra_args
                )
            return file_id, file_name, f'https://{self.bucket_name}.s3.ap-northeast-2.amazonaws.com/{file_id}
        except Exception as e:
            print(e)
            return None


    def download(self, file):
        self.s3_client.download_file(
            self.bucket_name,  # bucket
            str(file.file_key),  # key
            str(file.file_name)  # filename
        )



class PhotoView(APIView):
    def get(self, request, trip):
        #날짜별로 묶어서 리턴
        photos = Photo.objects.filter(trip=trip)
        dates = []
        for photo in photos:
            if photo.taken_at is None:
                dates.append(None)
            else:
                dates.append(photo.taken_at.date())

        data = []
        for date in set(dates):
            if date is None:
                data.append({
                    "date": None,
                    "photo": PhotoReturnSerializer(photos.filter(taken_at=None), many=True).data
                })
            else:
                data.append({
                    "date": date,
                    "photo": PhotoReturnSerializer(photos.filter(taken_at__day=date.day), many=True).data
                })
        response = {
            "status": status.HTTP_200_OK,
            "data": data
        }
        return Response(response)

    def post(self, request, trip):
        photos = request.FILES.getlist('photos')
        result_data = []
        s3_client = MyS3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)
        for photo in photos:
            taken_at = None

            img = Image.open(photo)
            img_info = img._getexif()

            try:
                for tag_id in img_info:
                    tag = TAGS.get(tag_id, tag_id)
                    img_data = img_info.get(tag_id)
                    if tag == 'DateTimeOriginal':
                        taken_at = datetime.strptime(img_data, '%Y:%m:%d %H:%M:%S')
                        print(taken_at)
            except Exception as e:
                print(e)

            photo.open()
            s3_result = s3_client.upload(photo)
            data = {
                "file_key": s3_result[0],
                "file_name": s3_result[1],
                "trip": trip,
                "url": s3_result[2],
                "taken_at": taken_at,
                "uploaded_by": request.user.id

            }

            serializer = PhotoUploadSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                result_data.append(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        response = {
            "status": status.HTTP_201_CREATED,
            "data": result_data
        }
        return Response(response)


class PhotoTagView(APIView):
    def patch(self, request, trip):
        photos = Photo.objects.filter(trip=trip).values_list('id', 'url')
        print(photos)
        trip_object = get_object_or_404(Trip, id=trip)
        number_of_people = Group.objects.filter(group_num=trip_object.group).count()
        # 모델 돌리기 (인자로 url 리스트, number_of_people) -> output: 태그 붙은 딕셔너리
        # output DB에 저장(수정)
        return Response({"사진 자동 분류가 완료되었습니다."}, status.HTTP_200_OK)


class PhotoTagDetailView(APIView):
    def get(self, request, trip, tag):
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

    def post(self, request, trip, tag):
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