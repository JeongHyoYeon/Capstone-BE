import requests
from tripfriend.settings import FLASK_IP
from rest_framework.response import Response
from rest_framework import status

def flask_post_request(endpoint, images):
    url = "http://" + FLASK_IP + "/" + endpoint
    data = {
        "image_list": images
    }

    try:
        response = requests.post(url=url, data=data)
        if response.status_code == 200:
            return response
        else:
            return Response({"요쳥 실패"}, status=status.HTTP_400_BAD_REQUEST)
    except requests.exceptions.RequestException as e:
        return Response({"요청 실패: " + e}, status=status.HTTP_400_BAD_REQUEST)

