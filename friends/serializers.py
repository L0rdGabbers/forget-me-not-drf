from rest_framework import serializers
from .models import FriendList, FriendRequest
from django.contrib.auth.models import User

class FriendListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = FriendList
        fields = ('owner', 'friends')

class SendFriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField()
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    is_active = serializers.ReadOnlyField()

    class Meta:
        model = FriendRequest
        fields = ('id', 'sender', 'receiver', 'is_active', 'created_at')

    def validate(self, data):
        sender = data['sender']
        receiver = data['receiver']
        if sender == receiver:
            raise ValidationError("Cannot send a friend request to yourself.")

        return data

    def create(self, validated_data):
        receiver = validated_data['receiver']
        sender = self.context['request'].user
        friend_request = FriendRequest.objects.create(sender=sender, receiver=receiver)
        return friend_request

class RespondToFriendRequestSerializer(serializers.ModelSerializer):
    cancel = serializers.BooleanField(write_only=True, required=False)
    accept = serializers.BooleanField(write_only=True, required=False)
    decline = serializers.BooleanField(write_only=True, required=False)
    sender = serializers.PrimaryKeyRelatedField(default=None, read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(default=None, read_only=True)
    is_active = serializers.ReadOnlyField()


    class Meta:
        model = FriendRequest
        fields = ('id', 'sender', 'receiver', 'is_active', 'created_at', 'cancel', 'accept', 'decline')


    def update(self, instance, validated_data):
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
            if user == instance.sender:
                self.fields['accept'].read_only = True
                self.fields['decline'].read_only = True
            elif user == instance.receiver:
                self.fields['cancel'].read_only = True
