from api.views import (CompanyInviteAPIView, CompanyJoinAPIView,
                       UserLoginAPIView, UserLogoutAPIView, UserSignupAPIView)
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
    path('users/signup/', UserSignupAPIView.as_view(), name='user_signup'),
    path('users/login/', UserLoginAPIView.as_view(), name='user_login'),
    path('users/logout/', UserLogoutAPIView.as_view(), name='user_logout'),
    path('company/users/invite/', CompanyInviteAPIView.as_view(), name='company_invite'),
    path('company/users/join/<str:token>/', CompanyJoinAPIView.as_view(), name='company_join'),
]
