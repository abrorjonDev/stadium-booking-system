from rest_framework.permissions import BasePermission

from apps.user.models import RoleChoice


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.role in {RoleChoice.OWNER, RoleChoice.ADMIN}
        )


class HasObjectOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user == obj.creator
            or request.user.is_admin
        )


class CanDeleteBooking(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user == obj.creator
            or request.user == obj.stadium.creator
            or request.user.is_admin
        )


class StadiumOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user.is_admin
            or request.user == obj.stadium.creator
        )