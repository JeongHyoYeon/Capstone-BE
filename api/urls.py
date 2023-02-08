from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from .views import login_views

urlpatterns = [
    path('register/', login_views.RegisterView.as_view()),
    path('login/', login_views.LoginView.as_view()),
    path('googlelogin/', login_views.GoogleLoginView.as_view()),
    path('login/refresh/', TokenRefreshView.as_view()),
    path('logout/', login_views.LogoutView.as_view()),
]