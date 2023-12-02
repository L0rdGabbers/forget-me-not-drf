from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    return obj.owner == request.user

class IsOwnerOrCollaboratorOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    return request.user == obj.owner | request.user in obj.collaborators

class SentFriendRequest(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return obj.sender == request.user