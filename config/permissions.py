from rest_framework.permissions import BasePermission

from cafe.models import Bartender, Cafe


class HasCafe(BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user.cafe:
                return True
        except:
            return False


class AllowToFastRegister(BasePermission):
    def has_permission(self, request, view):
        phone = request.data["phone"]

        if Cafe.objects.filter(phone=phone, owner__phone=phone).exists():
            return False
        if Bartender.objects.filter(phone=phone).exists():
            return False

        return True


class UnauthenticatedCreatePermission(BasePermission):
    def has_permission(self, request, view):
        return view.action == "create" or request.user and request.user.is_authenticated
