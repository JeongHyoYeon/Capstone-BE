from django.urls import path
from .views import *


urlpatterns = [
    # 여행 api
    path('trip/user/', PersonalTripView.as_view()),
    path('trip/<int:group>/', GroupTripView.as_view()),
    path('trip/detail/<int:trip>/', TripDetailView.as_view()),
    ]