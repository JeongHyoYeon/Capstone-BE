from django.urls import path
from .views import chatgpt_views, photo_views

urlpatterns = [
    # 사진 api
    # part는 yolo, face 또는 uploader
    path('<int:trip>/', photo_views.PhotoView.as_view()),
    path('<str:part>/<int:trip>/', photo_views.PhotoTagView.as_view()),
    path('<str:part>/<int:trip>/<int:tag>/', photo_views.PhotoTagDetailView.as_view()),
    path('<int:trip>/<str:user>/', photo_views.PhotoUploaderDetailView.as_view()),
    path('download/<int:photo>/', photo_views.PhotoDownloadView.as_view()),
    # chatGPT api
    path('search/<int:trip>/', chatgpt_views.PhotoSearchView.as_view())
]
