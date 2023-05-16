import requests
from tripfriend.settings import FLASK_HOST
from rest_framework.response import Response
from rest_framework import status

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

