from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .users_serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            if access_token:
                response.set_cookie('access', access_token, httponly=True, path='/')
            if refresh_token:
                response.set_cookie('refresh', refresh_token, httponly=True, path='/')

        return response


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    def post(self, request, *args, **kwargs):
        refresh_token = request.cookies.get('refresh')

        if not refresh_token:
            refresh_token = request.data.get('refresh')

        try:
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            response = Response({"detail": "성공적으로 로그아웃이 되었습니다."}, status=status.HTTP_200_OK)
            response.delete_cookie('access')
            response.delete_cookie('refresh')
            return response
        except Exception:
            response = Response({'detail': '로그아웃 처리되었습니다.'}, status=status.HTTP_200_OK)
            response.delete_cookie('access')
            response.delete_cookie('refresh')
            return response


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return Response({"detail": "성공적으로 삭제되었습니다."}, status=status.HTTP_200_OK)
