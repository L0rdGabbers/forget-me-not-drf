from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from friends.models import FriendList


class Profile(models.Model):
    """
    User profile model to store additional information about a user.
    """
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, default="")
    email = models.EmailField(max_length=255)
    image = models.ImageField(
        upload_to='images/', default='../i5d3k6odv5vkthh2yjul'
    )
    bio = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


def create_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a profile and friend list for a new user.
    """
    if created:
        # Create a profile for the user
        Profile.objects.create(owner=instance)
        # Create a friend list for the user
        FriendList.objects.create(owner=instance)


# Connect the signal to the User model
post_save.connect(create_profile, sender=User)
