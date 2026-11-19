from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Только владелец может редактировать/удалять."""
    message = 'Вы не являетесь владельцем этой привычки.'

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user