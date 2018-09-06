from rest_framework import permissions


class SelfPermission(permissions.BasePermission):
    """
    The user id is the same
    """
    def has_object_permission(self, request, view, object):
        return request.user.id == object.id
