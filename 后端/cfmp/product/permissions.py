from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    通用权限类：对于GET等只读操作允许任何人访问
    对于修改和删除操作，只允许资源的拥有者
    """

    message = "您没有权限执行此操作"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # 判断资源属于谁
        if hasattr(obj, "user"):
            return obj.user == request.user
        elif hasattr(obj, "collecter"):
            return obj.collecter == request.user

        return False
