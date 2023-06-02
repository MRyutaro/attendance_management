from api.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (Company, PaidLeave, PaidLeaveDays, PaidLeaveRecord, User,
                     WorkRecord)
from .serializers import (CompanySerializer, PaidLeaveDaysSerializer,
                          PaidLeaveRecordSerializer, PaidLeaveSerializer,
                          UserSerializer, WorkRecordSerializer)


class CompanyCreateAPIView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    # 同じメールアドレスが登録されていないか確認
    def post(self, request):
        company_email = request.data.get('company_email')
        company = Company.objects.filter(company_email=company_email).first()
        if company:
            return Response({'message': 'This email address is already registered.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().post(request)


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 同じメールアドレスが登録されていないか確認
    def post(self, request):
        user_email = request.data.get('user_email')
        user = User.objects.filter(user_email=user_email).first()
        if user:
            return Response({'message': 'This email address is already registered.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().post(request)


class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        company_id = request.data.get('company_id')
        user_email = request.data.get('user_email')
        # TODO: パスワードのハッシュ化
        user_login_password = request.data.get('user_login_password')

        # 会社が登録されていなかったら
        company = Company.objects.filter(company_id=company_id).first()
        if not company:
            return Response({'message': 'This company is not registered.'}, status=status.HTTP_400_BAD_REQUEST)

        # ユーザが登録されていなかったら
        user = User.objects.filter(company_id=company_id, user_email=user_email).first()
        if not user:
            return Response({'message': 'This user is not registered.'}, status=status.HTTP_400_BAD_REQUEST)

        # パスワードが間違っていたら
        user = User.objects.filter(company_id=company_id, user_email=user_email, user_login_password=user_login_password).first()
        if not user:
            return Response({'message': 'The password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        return Response({'company_id': company_id, 'user_id': user.user_id, 'is_active': user.is_active}, status=status.HTTP_200_OK)
