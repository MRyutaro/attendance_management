from api.models import User
from api.serializers import UserSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.


class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer = UserSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        # ユーザに対する追加の処理を行う場合はここに記述します

        return Response({'message': 'Login successful.'}, status=status.HTTP_200_OK)
