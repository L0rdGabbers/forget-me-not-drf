from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Any user may read acquire this code, but only the owner can edit or delete.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsSenderOrReceiver(permissions.BasePermission):
    """
    Only a friend request sender or receiver
    has object permission on this object.
    """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.sender or request.user == obj.receiver


class IsOwnerOrCollaborator(permissions.BasePermission):
    """
    Owners and Collaborators have permission to view,
    edit and delete this object
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        elif request.user in obj.collaborators.all():
            return True
        return False


class IsOwnerOrCollaboratorReadOnly(permissions.BasePermission):
    """
    Owners and Collaborators may view this code,
    but only the owner may edit or delete it.
    """
    def has_object_permission(self, request, view, obj):
        if (
            request.method in permissions.SAFE_METHODS
            and request.user in obj.collaborators.all()
        ):
            return True
        return obj.owner == request.user
