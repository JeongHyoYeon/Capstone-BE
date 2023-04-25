from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import login_views, group_views, trip_views, photo_views, photo_tag_views, chatgpt_views

urlpatterns = [
    # 로그인 api
    path('register/', login_views.RegisterView.as_view()),
    path('login/', login_views.LoginView.as_view()),
    path('googlelogin/', login_views.GoogleLoginView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('logout/', login_views.LogoutView.as_view()),
    # 그룹 api
    path('group/', group_views.GroupView.as_view()),
    path('group/invite/', group_views.GroupInviteListView.as_view()),
    path('group/invite/<int:usergroup>/', group_views.GroupInviteView.as_view()),
    # 여행 api
    path('trip/user/', trip_views.PersonalTripView.as_view()),
    path('trip/<int:group>/', trip_views.GroupTripView.as_view()),
    path('trip/detail/<int:trip>/', trip_views.TripDetailView.as_view()),
    # 사진 api
    # part는 yolo, face 또는 uploader
    path('photo/<int:trip>/', photo_views.PhotoView.as_view()),
    path('photo/<str:part>/<int:trip>/', photo_tag_views.PhotoTagView.as_view()),
    path('photo/<str:part>/<int:trip>/<int:tag>/', photo_tag_views.PhotoTagDetailView.as_view()),
    path('download/<int:photo>/', photo_views.PhotoDownloadView.as_view()),
    # chatGPT api
    path('photo-search/<int:trip>/', chatgpt_views.PhotoSearchView.as_view())
]
