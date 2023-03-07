from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime
from ..serializers import *
from datetime import datetime


class ExpenseView(APIView):
    def post(self, request, trip):
        try:
            expense_num = Expense.objects.latest('expense_num').expense_num + 1
        except Exception as e:
            print(e)
            expense_num = 1
        try:
            payed_at = request.data.get("payed_at")
        except Exception as e:
            print(e)
            payed_at = None
        participant_list = str(request.data.get("participant")).split()
        data_list = []
        for participant in participant_list:
            data = {
                "trip": trip,
                "expense_num": expense_num,
                "payer": request.data.get("payer"),
                "participant": participant,
                "payment": request.data.get("payment"),
                "payed_at": payed_at
            }
            serializer = ExpenseSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                data_list.append(data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        response = {
            'status': status.HTTP_201_CREATED,
            'data': data_list
        }
        print(response)
        return Response(response)


