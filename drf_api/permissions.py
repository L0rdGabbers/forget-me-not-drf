from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    return obj.owner == request.user

class IsSenderOrReceiver(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return obj.sender == request.user or obj.receiver == request.user

class IsOwnerOrCollaborator(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return request.user == obj.owner | request.user in obj.collaborators

class SentFriendRequest(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return obj.sender == request.user