from api.views import CompanyCreateAPIView, UserCreateAPIView, UserLoginAPIView
from django.urls import path

urlpatterns = [
    path('companies/signup/', CompanyCreateAPIView.as_view(), name='company_signup'),
    path('users/signup/', UserCreateAPIView.as_view(), name='user_signup'),
    path('users/login/', UserLoginAPIView.as_view(), name='user_login'),
]
