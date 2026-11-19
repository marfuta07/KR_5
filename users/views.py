from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserCreateSerializer

User = get_user_model()


class UserRegisterAPIView(generics.CreateAPIView):
    """Регистрация нового пользователя (открыта для всех)."""
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.AllowAny]
