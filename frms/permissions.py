from rest_framework import permissions

class IsSuperuser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsFinance(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'finance'

class IsCashier(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'cashier'
