from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

class FriendList(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="friend_list_owner")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    def __str__(self):
        return self.owner.username

    def add_friend(self, account):
        """
        Adds a new friend.
        """
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        """
        Removes a friend.
        """
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        """
        Unfriends another user
        """
        remover_friends_list = self
        remover_friends_list.remove_friend(removee)
        removee_friends_list = FriendList.objects.get(owner=removee)
        removee_friends_list.remove_friend(self.owner)

    def is_mutual_friend(self, friend):
        """
        Determines whether user and another profile are friends.
        """
        if friend in self.friends.all():
            return True
        return False

class FriendRequest(models.Model):
    """
    Allows a sender to send a friend request to a reciever.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        """
        Accept a friend request
        Updates both Sender and Receiver friend list
        """
        receiver_friend_list = FriendList.objects.get(owner=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(owner=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        """
        Decline a friend request
        Sets 'is_active' field to False
        """
        self.is_active = False
        self.save()

    def cancel(self):
        """
        Cancels a friend request
        Sets 'is_active' field to False
        """
        self.is_active = False
        self.save()