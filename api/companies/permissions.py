from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class CompanyObjectPermission(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'company_user')

    def has_object_permission(self, request, view, obj):
        if request.user.company_user.company.id != obj.id:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.company_user.is_admin


class IsCompanyUser(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'company_user')
