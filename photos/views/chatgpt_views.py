import openai
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from photos.models import *
from photos.serializers import PhotoReturnSerializer
from tripfriend.settings import OPENAI_KEY
from django.shortcuts import get_object_or_404
from base.permissions import GroupMembersOnly


class PhotoSearchView(APIView):
    permission_classes = [GroupMembersOnly]

    def post(self, request, trip):
        self.check_object_permissions(self.request, obj=get_object_or_404(Trip, id=trip))
        photos = Photo.objects.filter(trip=trip).values('id', 'uploaded_by__name', 'taken_at', 'tag_yolo__tag_name',
                                                        'tag_yolo__tag_name_kr', 'tag_face__custom_name')
        photo_list = str(list(photos))
        user_input = request.data['user_input']
        key_desc = "uploaded_by__name is the person who took the photo, taken_at is the date and time of shooting, " \
                   "tag_yolo__tag_name, tag_yolo__tag_name_kr is an object in the picture, i.e., " \
                   "a related element, and tag_face__custom_name is the name of the person in the picture"

        print(photo_list)
        openai.api_key = OPENAI_KEY
        chatgpt_output = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who returns ids separated by space."},
                {"role": "system", "content": "It's okay to be wrong, so use the information given to you "
                                              "to guess as much as possible and let me know"},
                {"role": "user", "content": "This is a list of photos and information about each photo"},
                {"role": "user", "content": "If you find the ids that fits the question return just the ids separated by space."},
                {"role": "user", "content": "Add no more words!"},
                {"role": "user", "content": photo_list},
                {"role": "user", "content": key_desc},
                {"role": "user", "content": user_input}
            ],
            temperature=0.2
        )
        output = chatgpt_output['choices'][0]['message']['content']
        data = []
        try:
            photo_id_list = output.split()
            for photo_id in photo_id_list:
                serializer = PhotoReturnSerializer(get_object_or_404(Photo, file_index=photo_id))
                data.append(serializer.data)

            response = {
                "status": status.HTTP_200_OK,
                "data": data
            }
            return Response(response)
        except Exception as e:
            print(e)
            return Response({output})

