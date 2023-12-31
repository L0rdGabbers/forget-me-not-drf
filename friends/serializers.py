from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import FriendList, FriendRequest
from django.contrib.auth.models import User
from django.db.models import Q


class FriendListSerializer(serializers.ModelSerializer):
    """
    Serializer for FriendList model.
    """

    owner = serializers.ReadOnlyField(source='owner.username')
    friend_details = serializers.SerializerMethodField()

    def get_friend_details(self, obj):
        """Retrieve friends and their details."""
        friends = obj.friends.all()
        friend_details = []

        for friend in friends:
            friend_request = FriendRequest.objects.filter(
                (Q(sender=obj.owner, receiver=friend) |
                 Q(sender=friend, receiver=obj.owner)),
                is_active=False
            ).first()

            if friend_request:
                friend_details.append({
                    'username': friend.username,
                    'id': self.get_friend_profile_id(friend_request),
                    'friend_id': friend_request.id,
                    'friend_image': friend.profile.image.url,
                })

        return friend_details

    def get_friend_profile_id(self, obj):
        """Get the friend's profile ID based on the friend request."""
        return obj.sender.id if (
            obj.receiver == self.context['request'].user) else obj.receiver.id

    class Meta:
        model = FriendList
        fields = ('owner', 'friend_details')


class FriendDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for FriendRequest model (detail view).
    """

    friend_profile_id = serializers.SerializerMethodField()
    friend_username = serializers.SerializerMethodField()
    unfriend = serializers.BooleanField(write_only=True, required=False)

    class Meta:
        model = FriendRequest
        fields = ('id', 'friend_profile_id', 'friend_username', 'unfriend')

    def get_friend_profile_id(self, obj):
        """Get the friend's profile ID based on the friend request."""
        return obj.sender.id if (
            obj.receiver == self.context['request'].user) else obj.receiver.id

    def get_friend_username(self, obj):
        """Get the friend's username based on the friend request."""
        return obj.sender.username if (
            obj.receiver == self.context['request'].user) else (
                obj.receiver.username)

    def update(self, instance, validated_data):
        """Handle unfriending based on 'unfriend' flag."""
        unfriend = validated_data.get('unfriend')

        if unfriend:
            instance.unfriend()

        return instance


class SendFriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for sending friend requests.
    """

    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    receiver = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=True)
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = FriendRequest
        fields = ('id', 'sender', 'receiver', 'is_active', 'created_at')

    def validate(self, data):
        """Ensure the sender and receiver are not the same user."""
        sender = data['sender']
        receiver = data['receiver']
        if sender == receiver:
            raise ValidationError("Cannot send a friend request to yourself.")

        return data

    def create(self, validated_data):
        """Create a new friend request."""
        receiver = validated_data['receiver']
        sender = self.context['request'].user
        friend_request = FriendRequest.objects.create(
            sender=sender, receiver=receiver)
        return friend_request


class FriendRequestListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing friend requests.
    """

    sender = serializers.PrimaryKeyRelatedField(default=None, read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(default=None, read_only=True)
    sender_username = serializers.SerializerMethodField()
    receiver_username = serializers.SerializerMethodField()

    def get_sender_username(self, obj):
        """Get the sender's username."""
        return obj.sender.username

    def get_receiver_username(self, obj):
        """Get the receiver's username."""
        return obj.receiver.username

    class Meta:
        model = FriendRequest
        fields = (
            'id', 'sender', 'receiver', 'sender_username', 'receiver_username',
            'is_active', 'created_at',)


class RespondToFriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for responding to friend requests.
    """

    cancel = serializers.BooleanField(write_only=True, required=False)
    accept = serializers.BooleanField(write_only=True, required=False)
    decline = serializers.BooleanField(write_only=True, required=False)
    sender = serializers.PrimaryKeyRelatedField(default=None, read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(default=None, read_only=True)
    sender_username = serializers.SerializerMethodField()
    receiver_username = serializers.SerializerMethodField()
    is_active = serializers.ReadOnlyField()

    def get_sender_username(self, obj):
        """Get the sender's username."""
        return obj.sender.username

    def get_receiver_username(self, obj):
        """Get the receiver's username."""
        return obj.receiver.username

    class Meta:
        model = FriendRequest
        fields = (
         'id', 'sender', 'receiver', 'sender_username',
         'receiver_username', 'is_active', 'created_at', 'cancel', 'accept',
         'decline'
        )

    def update(self, instance, validated_data):
        """Handle request based on 'cancel', 'accept', or 'decline'."""
        cancel = validated_data.get('cancel')
        accept = validated_data.get('accept')
        decline = validated_data.get('decline')

        if cancel:
            instance.cancel()
        elif accept:
            instance.accept()
        elif decline:
            instance.decline()

        return instance

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        user = self.context['request'].user
        instance = kwargs.get('instance')

        if instance:
            # Set read-only flags based on user's role in the friend request
            if user == instance.sender:
                self.fields['accept'].read_only = True
                self.fields['decline'].read_only = True
            elif user == instance.receiver:
                self.fields['cancel'].read_only = True
