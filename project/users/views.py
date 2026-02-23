from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer

class RegisterView(generics.CreateAPIView):
    # 3. 가져온 User 모델을 직접 사용합니다.
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]