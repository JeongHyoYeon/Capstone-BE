import openai
from rest_framework.views import APIView
from api.models import *
from tripfriend.settings import OPENAI_KEY


openai.api_key = OPENAI_KEY

response = openai.Completion.create(
    # 인자 조정해야
    model="text-davinci-003",
    prompt="Hi my name is Jeonghyun Lee",  # 들어갈 내용 구상...
    temperature=0,  # 0: 매 프롬프트마다 동일한 답변, 1: 매 프롬프트마다 상이한 답변
    max_tokens=100,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    stop=["\n"]
)

print(response)  # 원하는 부분 잘라야


class FindPhotoView(APIView):
    def post(self, request, trip):
        photos = Photo.objects.filter(trip=trip).values_list('id', 'uploaded_by', 'taken_at', 'category_cv')
        user_input = request.data['user_input']
        chatGPT_input = "uploaded_by는 찍은 사람을 뜻하고 category_cv는 관련된 요소라고할 때, " + user_input\
                        + "위에 준 리스트에서 해당되는 항목의 id만 띄어쓰기로 구분해서 알려줘."
