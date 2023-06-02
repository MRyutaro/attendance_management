from api.views import LoginView, UserCreateAPIView
from django.urls import path

urlpatterns = [
    path('signup/', UserCreateAPIView.as_view(), name='user_signup'),
    path('login/', LoginView.as_view(), name='user_login'),
]
