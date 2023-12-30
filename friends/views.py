from django.http import Http404
from django.core.exceptions import ValidationError
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FriendList, FriendRequest
from .serializers import (
    FriendListSerializer, FriendDetailSerializer, SendFriendRequestSerializer,
    RespondToFriendRequestSerializer, FriendRequestListSerializer
)
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from drf_api.permissions import IsSenderOrReceiver


class FriendListView(generics.RetrieveAPIView):
    """
    Retrieve the friend list for the authenticated user.
    """
    serializer_class = FriendListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return FriendList.objects.get(owner=self.request.user)
        except FriendList.DoesNotExist:
            raise Http404


class FriendDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update a friend request's details.
    """
    serializer_class = FriendDetailSerializer
    permission_classes = [IsSenderOrReceiver, permissions.IsAuthenticated]

    def get_object(self):
        friend_request_id = self.kwargs['pk']
        try:
            friend_request = FriendRequest.objects.get(
                Q(sender=self.request.user) | Q(receiver=self.request.user),
                id=friend_request_id
            )
            return friend_request
        except FriendRequest.DoesNotExist:
            raise Http404("FriendRequest does not exist")


class SendFriendRequestView(generics.CreateAPIView):
    """
    Send a friend request to another user.
    """
    serializer_class = SendFriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        receiver = serializer.validated_data['receiver']
        sender = self.request.user

        # Checks if friend request to this user already exists
        existing_request = FriendRequest.objects.filter(
            sender=sender, receiver=receiver, is_active=True)
        if existing_request.exists():
            return Response(
                {"detail": "A friend reques already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the receiver is already in the friend list
        if sender.friends.filter(pk=receiver.pk).exists():
            return Response(
                {"detail": "The receiver is already in the friend list."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if the receiver has sent a friend request to the sender
        reciprocal_request = FriendRequest.objects.filter(
            sender=receiver, receiver=sender, is_active=True)
        if reciprocal_request.exists():
            return Response(
                {"detail": "The receiver already sent you a friend request."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Save the friend request
        self.perform_create(serializer)

        return Response(
            {"detail": "Friend request sent successfully."},
            status=status.HTTP_201_CREATED
        )

    def perform_create(self, serializer):
        receiver = serializer.validated_data['receiver']
        sender = self.request.user
        serializer.save(sender=sender, receiver=receiver)


class RespondToFriendRequestView(generics.RetrieveUpdateDestroyAPIView):
    """
    Accept, decline, or cancel a friend request.
    """
    serializer_class = RespondToFriendRequestSerializer
    permission_classes = [IsSenderOrReceiver, permissions.IsAuthenticated]

    queryset = FriendRequest.objects.all()

    def get_object(self):
        friend_request_id = self.kwargs['pk']
        try:
            friend_request = FriendRequest.objects.get(
                Q(sender=self.request.user) | Q(receiver=self.request.user),
                id=friend_request_id
            )
            return friend_request
        except FriendRequest.DoesNotExist:
            raise Http404("FriendRequest does not exist")

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.is_active:
            instance.accept()
        elif instance.is_active is False:
            instance.decline()


class FriendRequestListView(generics.ListAPIView):
    """
    List friend requests for the authenticated user.
    """
    serializer_class = FriendRequestListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(
            Q(receiver=self.request.user, is_active=True) |
            Q(sender=self.request.user, is_active=True)
        )
