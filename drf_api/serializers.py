from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers
from profiles.serializers import ProfileSerializer
from profiles.models import Profile


class CurrentUserSerializer(UserDetailsSerializer):
    profile = ProfileSerializer(source='profile', read_only=True)

    class Meta(UserDetailsSerializer.Meta):
        fields = UserDetailsSerializer.Meta.fields + ('profile',)