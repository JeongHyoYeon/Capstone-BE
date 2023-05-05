from datetime import datetime
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..serializers import *
from api.mys3client import MyS3Client
from tripfriend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME
from PIL import Image
from PIL.ExifTags import TAGS
from api.permissions import GroupMembersOnly
import base64


class PhotoView(APIView):
    permission_classes = [GroupMembersOnly]

    def get(self, request, trip):
        self.check_object_permissions(self.request, obj=get_object_or_404(Trip, id=trip))
        # 날짜별로 묶어서 리턴
        photos = Photo.objects.filter(trip=trip)
        dates = []
        data = [{
            "date": None,
            "photo": []
        }]

        for photo in photos:
            if photo.taken_at is None:
                data[0]["photo"].append(
                    PhotoReturnSerializer(photo).data
                )
            else:
                dates.append(photo.taken_at.date())

        for date in sorted(set(dates)):
            data.append({
                "date": date,
                "photo": PhotoReturnSerializer(photos.filter(taken_at__day=date.day), many=True).data
            })

        data.reverse()
        response = {
            "status": status.HTTP_200_OK,
            "data": data
        }
        return Response(response)

    def post(self, request, trip):
        self.check_object_permissions(self.request, obj=get_object_or_404(Trip, id=trip))
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
            file_name = photo.name
            s3_result = s3_client.upload(photo)
            data = {
                "file_key": s3_result[0],
                "file_name": file_name,
                "trip": trip,
                "url": s3_result[1],
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


class PhotoDownloadView(APIView):
    permission_classes = [GroupMembersOnly]

    def get(self, request, photo):
        photo = get_object_or_404(Photo, id=photo)
        self.check_object_permissions(self.request, obj=get_object_or_404(Trip, id=photo.trip_id))
        serializer = PhotoReturnSerializer(photo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, photo):
        # 다운로드 받기
        photo = get_object_or_404(Photo, id=photo)
        self.check_object_permissions(self.request, obj=get_object_or_404(Trip, id=photo.trip_id))
        # URL 보내는 방법
        return Response(PhotoReturnSerializer(photo).data, status=status.HTTP_200_OK)

        # File 객체 보내는 방법
        # s3_client = MyS3Client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME)
        # image = s3_client.get_file(photo.file_key)
        # image_data = image.get()['Body'].read()
        # encoded_image = base64.b64encode(image_data).decode('utf-8')
        # print(image.content_type)
        # return Response(
        #     encoded_image, status=status.HTTP_200_OK,
        #     content_type=image.content_type,
        #     headers={
        #     'Content-Disposition': f'attachment; filename="{photo.file_name}"'
        #     }
        # )
        # return response


