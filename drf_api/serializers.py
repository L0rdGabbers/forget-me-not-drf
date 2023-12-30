from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework import serializers


class CurrentUserSerializer(UserDetailsSerializer):
    # Additional fields for the CurrentUserSerializer
    id = serializers.ReadOnlyField(source='profile.id')
    profile_image = serializers.ReadOnlyField(source='profile.image.url')
    is_owner = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()

    # Method to determine if the user is the owner of their profile
    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.profile.owner

    # Method to get the user's bio from their profile
    def get_bio(self, obj):
        return obj.profile.bio

    class Meta(UserDetailsSerializer.Meta):
        # Include the additional fields in the serializer's Meta class
        fields = UserDetailsSerializer.Meta.fields + (
            'id', 'profile_image', 'is_owner', 'bio'
        )
