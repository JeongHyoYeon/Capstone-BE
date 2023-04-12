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
        photos = Photo.objects.filter(trip=trip).values('file_index', 'uploaded_by__name',
                                                        'taken_at', 'category_yolo', 'category_face')
        print(photos)
        user_input = request.data['user_input']
        chatgpt_input = str(photos) + "\nuploaded_by__name는 찍은 사람을 뜻하고 taken_at은 촬영 시간을 뜻해. " \
                                      "그리고 category_yolo는 관련된 요소라고할 때, " + user_input\
                        + ". 위에 준 리스트에서 해당되는 항목의 file_index만 띄어쓰기로 구분해서 알려줘."
        print(chatgpt_input)
        openai.api_key = OPENAI_KEY
        chatgpt_output = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": chatgpt_input}
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

