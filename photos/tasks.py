from __future__ import absolute_import, unicode_literals
import requests
from tripfriend.settings import FLASK_HOST
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from celery import shared_task
from .models import *
from django_celery_results.models import TaskResult

@shared_task
def flask_post_request(endpoint, images):
    url = "http://" + FLASK_HOST + "/" + endpoint
    data = {
        "image_list": list(images)
    }

    try:
        response = requests.post(url=url, json=data)
        if response.status_code == 200:
            return response
        else:
            return Response({"요쳥 실패"}, status=response.status_code)
    except requests.exceptions.RequestException as e:
        return Response({"요쳥 실패: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)

@shared_task
def save_results(task_id):  # 콜백 함수
    result = TaskResult.objects.get(task_id=task_id).result
    if result.status_code == 200:
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