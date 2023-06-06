from api.views import (
    CompanyCreateAPIView, CompanyUpdateAPIView,
    UserCreateAPIView, UserLoginAPIView
)
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    path('auth/', include('djoser.urls.jwt')),
    path('companies/signup/', CompanyCreateAPIView.as_view(), name='company_signup'),
    path('companies/update/', CompanyUpdateAPIView.as_view(), name='company_update'),
    path('users/signup/', UserCreateAPIView.as_view(), name='user_signup'),
    path('users/login/', UserLoginAPIView.as_view(), name='user_login'),
]
