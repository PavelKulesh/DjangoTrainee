from rest_framework.permissions import BasePermission


class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        return request.user.is_superuser


class IsSuperUserOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj == request.user

    def has_permission(self, request, view):
        if request.method in ['GET', 'PATCH', 'HEAD', 'OPTIONS'] and request.user.id:
            return True
        elif request.method == 'POST' and not request.user.id:
            return True

        return request.user.is_superuser


class IsSuperUserOrOwnerReadOnly(IsSuperUserOrOwner):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        return obj.customer_id == request.user.id

    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS'] and request.user.id:
            return True

        return request.user.is_superuser


class IsSuperUserOrOwnerAndEmailConfirmed(IsSuperUserOrOwnerReadOnly):
    def has_permission(self, request, view):
        if (request.method in ['GET', 'HEAD', 'OPTIONS'] and request.user.id) or (
                request.method in ['POST', 'PATCH', 'DELETE'] and request.user.id and request.user.is_confirmed):
            return True

        return request.user.is_superuser
