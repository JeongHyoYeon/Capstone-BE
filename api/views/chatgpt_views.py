import openai
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import *
from api.serializers import PhotoReturnSerializer
from tripfriend.settings import OPENAI_KEY
from django.shortcuts import get_object_or_404


class PhotoSearchView(APIView):
    def post(self, request, trip):
        photos = Photo.objects.filter(trip=trip).values('id', 'uploaded_by__name', 'taken_at',
                                                        'tag_yolo__tag_name', 'tag_face__custom_name')
        photo_list = str(photos)
        user_input = request.data['user_input']
        key_desc = "uploaded_by__name는 찍은 사람을 뜻하고 taken_at은 촬영 시간, tag_yolo는 관련 요소를 뜻해"

        print(photo_list)
        openai.api_key = OPENAI_KEY
        chatgpt_output = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who returns file indexes separated by space."},
                {"role": "user", "content": "다음 리스트에서 해당되는 항목의 file_index만 띄어쓰기로 구분해서 알려줘"},
                {"role": "user", "content": photo_list},
                {"role": "user", "content": key_desc},
                {"role": "user", "content": user_input}
            ]
        )
        photo_id_list = chatgpt_output['choices'][0]['message']['content'].split()

        data = []
        for photo_id in photo_id_list:
            serializer = PhotoReturnSerializer(get_object_or_404(Photo, file_index=photo_id))
            data.append(serializer.data)

        response = {
            "status": status.HTTP_200_OK,
            "data": data
        }
        return Response(response)

