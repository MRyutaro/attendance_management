from api.views import (CompanyCreateAPIView, CompanyUpdateAPIView,
                       UserCreateAPIView, UserLoginAPIView, UserLogoutAPIView)
from django.urls import path
from django.views.generic import RedirectView
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

urlpatterns = [
    path('', RedirectView.as_view(url='docs/', permanent=True)),
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
    path('companies/signup/', CompanyCreateAPIView.as_view(), name='company_signup'),
    path('companies/update/', CompanyUpdateAPIView.as_view(), name='company_update'),
    path('users/signup/', UserCreateAPIView.as_view(), name='user_signup'),
    path('users/login/', UserLoginAPIView.as_view(), name='user_login'),
    path('users/logout/', UserLogoutAPIView.as_view(), name='user_logout'),
]