import requests
from tripfriend.settings import FLASK_IP
from rest_framework.response import Response


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
            return Response({"요쳥 실패"})
    except requests.exceptions.RequestException as e:
        return e

