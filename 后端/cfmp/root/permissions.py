from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    自定义权限类，仅允许 privilege == 1 的用户访问。
    """

    def has_permission(self, request, view):
        # 检查用户是否是认证用户，并且其 privilege 等于 1
        return request.user and request.user.privilege == 1