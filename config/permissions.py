from rest_framework.permissions import BasePermission

class HasCafe(BasePermission):

    def has_permission(self, request, view):
        try:
            if request.user.cafe : return True
        except : return False