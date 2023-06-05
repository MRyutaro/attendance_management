from api.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import (Company, PaidLeave, PaidLeaveDay, PaidLeaveRecord, User,
                     WorkRecord)
from .serializers import (CompanySerializer, PaidLeaveDaySerializer,
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
        # requestのpassword以外のデータを返す
        company_name = request.data.get('company_name')
        company = Company.objects.create(
            company_name=company_name, company_email=company_email, company_login_password=request.data.get('company_login_password'))
        return Response({'company_name': company_name, 'company_email': company_email}, status=status.HTTP_200_OK)


class CompanyUpdateAPIView(APIView):
    # TODO: 1つ1つ例外処理を書くのは面倒なので、まとめて書けないか調べる
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    # 同じメールアドレスが登録されていないか確認
    def put(self, request):
        company_email = request.data.get('company_email')
        company = Company.objects.filter(company_email=company_email).first()

        if not company:
            return Response({'message': 'This email address is not registered.'}, status=status.HTTP_400_BAD_REQUEST)

        company_login_password = request.data.get('company_login_password')
        if company.company_login_password != company_login_password:
            return Response({'message': 'The password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        # 会社名が変更されていたら
        new_company_name = request.data.get('company_name')
        old_company_name = company.company_name
        if new_company_name is None:
            return Response({'message': 'The company name is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_company_name != old_company_name:
            company.company_name = new_company_name
            company.save()
            return Response({'message': 'The company name has been changed.'}, status=status.HTTP_200_OK)

        return Response({'message': 'No changes have been made.'}, status=status.HTTP_200_OK)


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # 同じメールアドレスが登録されていないか確認
    def post(self, request):
        user_email = request.data.get('user_email')
        user = User.objects.filter(user_email=user_email).first()
        if user:
            return Response({'message': 'This email address is already registered.'}, status=status.HTTP_400_BAD_REQUEST)

        user_name = request.data.get('user_name')
        user_login_password = request.data.get('user_login_password')
        authority = request.data.get('authority')
        # TODO: もし交通費がなかったら0を入れる
        # TODO: もし交通費が0より小さかったらエラーを返す
        commuting_expenses = request.data.get('commuting_expenses')
        print(f"commuting_expenses: {commuting_expenses}")
        if commuting_expenses is str:
            return Response({'message': 'The commuting_expenses must be integer.'}, status=status.HTTP_400_BAD_REQUEST)
        elif commuting_expenses is None or commuting_expenses == '':
            commuting_expenses = 0
        else:
            commuting_expenses = int(commuting_expenses)

        company_id = request.data.get('company')
        company = Company.objects.get(company_id=company_id)

        user = User.objects.create(
            user_name=user_name, user_email=user_email, user_login_password=user_login_password, authority=authority, commuting_expenses=commuting_expenses, company=company
        )
        return Response({'user_name': user_name, 'user_email': user_email}, status=status.HTTP_200_OK)


class UserLoginAPIView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        company_id = request.data.get('company')
        user_email = request.data.get('user_email')
        # TODO: パスワードのハッシュ化
        user_login_password = request.data.get('user_login_password')

        # 会社が登録されていなかったら
        print(f"company_id: {company_id}")
        company = Company.objects.filter(company_id=company_id).first()
        if not company:
            return Response({'message': 'This company is not registered.'}, status=status.HTTP_400_BAD_REQUEST)

        # ユーザが登録されていなかったら
        user = User.objects.filter(company_id=company_id, user_email=user_email).first()
        if not user:
            return Response({'message': 'This user is not registered.'}, status=status.HTTP_400_BAD_REQUEST)

        # パスワードが間違っていたら
        user = User.objects.filter(company=company, user_email=user_email, user_login_password=user_login_password).first()
        if not user:
            return Response({'message': 'The password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)

        user.is_active = True
        user.save()
        return Response({'company_id': company.company_id, 'user_id': user.user_id, 'is_active': user.is_active}, status=status.HTTP_200_OK)
