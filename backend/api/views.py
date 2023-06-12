from django.contrib.sessions.backends.db import SessionStore
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (Company, PaidLeave, PaidLeaveDay, PaidLeaveRecord, User,
                     WorkRecord)
from .serializers import (
    CompanySerializer, PaidLeaveDaySerializer,
    PaidLeaveRecordSerializer, PaidLeaveSerializer,
    UserSerializer, WorkRecordSerializer
)
from rest_framework.permissions import AllowAny
from .permissions import IsLoggedInUser


class CompanyCreateAPIView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    # 同じメールアドレスが登録されていないか確認
    def post(self, request):
        email = request.data.get('email')
        company = Company.objects.filter(email=email).first()
        if company:
            return Response({'message': 'This email address is already registered.'}, status=status.HTTP_400_BAD_REQUEST)
        # requestのpassword以外のデータを返す
        name = request.data.get('name')
        company = Company.objects.create(
            email=email, name=name, password=request.data.get('password'))
        return Response({'company_name': name, 'company_email': email}, status=status.HTTP_200_OK)


class CompanyUpdateAPIView(APIView):
    # TODO: 1つ1つ例外処理を書くのは面倒なので、まとめて書けないか調べる
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    # 同じメールアドレスが登録されていないか確認
    def put(self, request):
        email = request.data.get('email')
        company = Company.objects.get(email=email)
        if not company:
            return Response({'message': 'This email address is not registered.'}, status=status.HTTP_400_BAD_REQUEST)

        input_password = request.data.get('password')

        if input_password == company.password:
            try:
                company_name = request.data.get('name')
                company.name = company_name
                company.save()
                return Response({'company_name': company_name}, status=status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'message': 'Company name is not updated.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        # TODO: これはSerializerでやるべき
        # 同じメールアドレスが登録されていないか確認
        email = request.data.get('user_email')
        user = User.objects.filter(email=email).first()
        if user:
            return Response({'message': 'This email address is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')

        company_id = request.data.get('company_id')
        company = Company.objects.get(pk=company_id)

        user = User.objects.create_user(
            company=company, email=email, password=password
        )
        return Response({'user_email': email}, status=status.HTTP_200_OK)


class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        company_id = request.data.get('company')
        email = request.data.get('email')
        password = request.data.get('password')

        # 会社が登録されていなかったら
        company = Company.objects.get(pk=company_id)
        if not company:
            return Response({'message': 'This company is not registered.'}, status=status.HTTP_400_BAD_REQUEST)

        # ユーザが登録されていなかったら
        user = User.objects.get(company=company, email=email)
        if not user:
            return Response({'message': 'This user is not registered.'}, status=status.HTTP_400_BAD_REQUEST)

        # パスワードが間違っていたら
        if not user.check_password(password):
            return Response({'message': 'The password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()

        # セッションにユーザ情報を保存
        session = SessionStore()
        session['user_id'] = user.pk
        session['company_id'] = company.pk
        session.save()

        response = Response({'company_id': company.pk, 'user_id': user.pk, 'is_active': user.is_active}, status=status.HTTP_200_OK)

        # セッションIDをクッキーに設定
        response.set_cookie('sessionid', session.session_key)

        return response


class UserLogoutAPIView(APIView):
    permission_classes = [IsLoggedInUser]

    def post(self, request):
        sessionid = request.COOKIES.get('sessionid')
        # SessionStore(session_key=sessionid).items()の中身にidが入ってる。
        session = SessionStore(session_key=sessionid)
        # サーバー側のセッションを削除
        session.delete()
        response = Response({'message': 'Logout successfully.'}, status=status.HTTP_200_OK)
        # クライアント側のセッションを削除
        response.delete_cookie('sessionid')
        return response
