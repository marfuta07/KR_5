from rest_framework import viewsets, permissions
from django.db import models
from .models import Habit
from .serializers import HabitSerializer
from .paginators import HabitPagination
from .permissions import IsOwner


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        user = self.request.user
        if self.action in ['list', 'retrieve']:
            return Habit.objects.filter(
                models.Q(owner=user) | models.Q(is_public=True)
            ).distinct()
        return Habit.objects.filter(owner=user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
