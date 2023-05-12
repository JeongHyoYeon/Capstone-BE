from django.urls import path
from .views import trip_views, chatgpt_views, photo_views

urlpatterns = [
    # 여행 api
    path('trip/user/', trip_views.PersonalTripView.as_view()),
    path('trip/<int:group>/', trip_views.GroupTripView.as_view()),
    path('trip/detail/<int:trip>/', trip_views.TripDetailView.as_view()),
    # 사진 api
    # part는 yolo, face 또는 uploader
    path('photo/<int:trip>/', photo_views.PhotoView.as_view()),
    path('photo/<str:part>/<int:trip>/', photo_views.PhotoTagView.as_view()),
    path('photo/<str:part>/<int:trip>/<int:tag>/', photo_views.PhotoTagDetailView.as_view()),
    path('uploader/<int:trip>/<str:user>/', photo_views.PhotoUploaderDetailView.as_view()),
    path('download/<int:photo>/', photo_views.PhotoDownloadView.as_view()),
    # chatGPT api
    path('search/<int:trip>/', chatgpt_views.PhotoSearchView.as_view())
]
