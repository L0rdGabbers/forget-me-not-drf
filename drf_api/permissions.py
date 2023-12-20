from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.method in permissions.SAFE_METHODS:
      return True
    return obj.owner == request.user

class IsSenderOrReceiver(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return request.user == obj.sender or request.user == obj.receiver

class IsOwnerOrCollaborator(permissions.BasePermission):
  def has_permission(self, request, view):
    if request.method in permissions.SAFE_METHODS:
      return True
    return request.user and request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    if request.user == obj.owner:
      return True
    elif request.user in obj.collaborators.all() and request.method != 'DELETE':
      return True
    return False


class IsOwnerOrCollaboratorReadOnly(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    if request.user == obj.owner:
      return True
    if request.method in permissions.SAFE_METHODS and request.user in obj.collaborators.all():
      return True
    return False

class SentFriendRequest(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    return obj.sender == request.user