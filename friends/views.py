from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from .models import FriendList, FriendRequest
from .serializers import FriendListSerializer, SendFriendRequestSerializer, RespondToFriendRequestSerializer
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated


from .serializers import FriendListSerializer

class FriendListView(generics.RetrieveAPIView):
    """
    Retrieve the friend list for the authenticated user.
    """
    serializer_class = FriendListSerializer
    permission_classes = [IsAuthenticated]


    def get_object(self):
        try:
            return FriendList.objects.get(owner=self.request.user)
        except FriendList.DoesNotExist:
            raise Http404("You do not have any friends yet. But don't worry, you just need to start making some requests!")

class SendFriendRequestView(generics.CreateAPIView):
    """
    Send a friend request to another user.
    """
    serializer_class = SendFriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        receiver = serializer.validated_data['receiver']
        sender = self.request.user
        serializer.save(sender=sender, receiver=receiver)

class RespondToFriendRequestView(generics.RetrieveUpdateDestroyAPIView):
    """
    Accept, decline, or cancel a friend request.
    """
    serializer_class = RespondToFriendRequestSerializer

    queryset = FriendRequest.objects.all()  # Make sure to adjust the queryset as needed

    def get_object(self):
        friend_request_id = self.kwargs['pk']
        try:
            friend_request = FriendRequest.objects.get(
                Q(sender=self.request.user) | Q(receiver=self.request.user),
                id=friend_request_id
            )
            return friend_request
        except FriendRequest.DoesNotExist:
            # Handle the case where the friend request does not exist
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
    serializer_class = SendFriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(receiver=self.request.user, is_active=True)