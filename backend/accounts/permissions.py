from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    message = "Accès réservé à l'administrateur."
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "ADMIN"
        )