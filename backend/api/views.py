from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.translation import gettext_lazy as _

from .models import Invitation
from .serializers import (
    UserSerializer, InvitationSerializer, JoinSerializer
)
from .exceptions import InvalidTokenError, ExpriedTokenError, UserDoesNotExistError, AlreadyBelongsError
from rest_framework.permissions import AllowAny, IsAuthenticated


class UserSignupAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserLoginAPIView(APIView):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'message': 'ログインに成功しました。'})
        else:
            return Response({'message': 'ログインに失敗しました。'}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        logout(request)
        return Response({'message': 'ログアウトしました。'})


# 会社に招待する
class CompanyInviteAPIView(APIView):
    serializer_class = InvitationSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        invitee_email = request.data.get('invitee_email')
        if not invitee_email:
            return Response({'error': '招待するメールアドレスを入力してください。'}, status=400)

        serializer = InvitationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '招待を送信しました。'})
        else:
            return Response(serializer.errors, status=400)


# 招待URLから会社に参加する
class CompanyJoinAPIView(APIView):
    serializer_class = JoinSerializer
    permission_classes = (AllowAny,)

    def post(self, request, token):
        invitation = get_object_or_404(Invitation, token=token)
        serializer = JoinSerializer(data=request.data, context={'invitation': invitation})

        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {'status': 'success', 'message': '会社に参加しました。'},
                    status=status.HTTP_201_CREATED
                )
            except InvalidTokenError as e:
                error_class = e.__class__.__name__
                error_message = e.args[0]
                return Response(
                    {'status': 'fail', 'error_class': error_class, 'message': error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except ExpriedTokenError as e:
                error_class = e.__class__.__name__
                error_message = e.args[0]
                return Response(
                    {'status': 'fail', 'error_class': error_class, 'message': error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except UserDoesNotExistError as e:
                error_class = e.__class__.__name__
                error_message = e.args[0]
                return Response(
                    {'status': 'fail', 'error_class': error_class, 'message': error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )
            except AlreadyBelongsError as e:
                error_class = e.__class__.__name__
                error_message = e.args[0]
                return Response(
                    {'status': 'fail', 'error_class': error_class, 'message': error_message},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {'status': 'fail', 'message': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
