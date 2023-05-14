from django.urls import path
from .views import chatgpt_views, photo_views

urlpatterns = [
    # 사진 api
    path('<int:trip>/', photo_views.PhotoView.as_view()),

    # 폴더 밖
    path('face/<int:trip>/', photo_views.PhotoFaceView.as_view()),
    path('yolo/<int:trip>/', photo_views.PhotoYoloView.as_view()),
    path('uploader/<int:trip>/', photo_views.PhotoUploaderView.as_view()),

    # 폴더 안
    path('face/<int:trip>/<int:tag>/', photo_views.PhotoFaceDetailView.as_view()),
    path('yolo/<int:trip>/<int:tag>/', photo_views.PhotoYoloDetailView.as_view()),
    path('uploader/<int:trip>/<str:user>/', photo_views.PhotoUploaderDetailView.as_view()),

    # 개별 사진
    path('download/<int:photo>/', photo_views.PhotoDownloadView.as_view()),

    # chatGPT api
    path('search/<int:trip>/', chatgpt_views.PhotoSearchView.as_view())
]
