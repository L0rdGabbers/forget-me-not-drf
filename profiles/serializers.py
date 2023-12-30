from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model to convert data to/from JSON.
    """
    # Convert owner field to read-only and use username as the representation
    owner = serializers.ReadOnlyField(source='owner.username')

    # Custom field to check if the authenticated user is owner of the profile
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Method to determine if the authenticated user is owner of the profile.
        """
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = [
            'id', 'owner', 'created_at',
            'updated_at', 'image', 'is_owner', 'bio'
        ]
