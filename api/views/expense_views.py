from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils.timezone import localtime
from ..serializers import *
from datetime import datetime


class ExpenseView(APIView):
    def get(self, request, trip):
        expense_list = Expense.objects.filter(trip=trip)
        serializer = ExpenseSerializer(expense_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def patch(self, request):
        expense_instance = get_object_or_404(Expense, id=request.data['id'])
        serializer = ExpenseSerializer(instance=expense_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseCategoryView(APIView):
    def get(self, request, trip, category):
        expense_list = Expense.objects.filter(trip=trip, category=category)
        serializer = ExpenseSerializer(expense_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    