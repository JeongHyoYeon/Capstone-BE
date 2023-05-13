from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from accounts.views import user_views, group_views

urlpatterns = [
    # 유저(로그인) api
    path('register/', user_views.RegisterView.as_view()),
    path('login/', user_views.LoginView.as_view()),
    path('googlelogin/', user_views.GoogleLoginView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('logout/', user_views.LogoutView.as_view()),
    # 그룹 api
    path('group/', group_views.GroupView.as_view()),
    path('invite/', group_views.GroupInviteListView.as_view()),
    path('invite/<int:usergroup>/', group_views.GroupInviteView.as_view())
]