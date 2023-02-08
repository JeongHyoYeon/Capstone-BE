from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import login_views, group_views

urlpatterns = [
    # 로그인 api
    path('register/', login_views.RegisterView.as_view()),
    path('login/', login_views.LoginView.as_view()),
    path('googlelogin/', login_views.GoogleLoginView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('logout/', login_views.LogoutView.as_view()),
    # 그룹 api
    path('group/new/', group_views.NewGroupView.as_view()),
    path('group/invite/', group_views.GroupView.as_view())
]