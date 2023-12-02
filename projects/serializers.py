from rest_framework import serializers
from .models import Project
from django.contrib.auth.models import User

class ProjectListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    collaborators = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    is_collaborator = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    complete = serializers.BooleanField(read_only=True)

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_is_collaborator(self, obj):
        request = self.context['request']
        return request.user in obj.collaborators.all()

    class Meta:
        model = Project
        fields = [
            'id', 'owner', 'profile_id', 'title', 'summary', 'collaborators', 'due_date', 'complete', 'image', 'created_at', 'updated_at', 'profile_image', 'is_owner', 'is_collaborator'
        ]

class ProjectDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    collaborators = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    collaborator_usernames = serializers.SerializerMethodField()
    is_collaborator = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')

    def validate_image(self, value):
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError(
                'Image size larger than 2MB!'
            )
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!'
            )
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!'
            )
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_is_collaborator(self, obj):
        request = self.context['request']
        return request.user in obj.collaborators.all()

    def get_collaborator_usernames(self, obj):
        collaborators = obj.collaborators.all()
        collaborator_usernames = [collaborator.username for collaborator in collaborators]
        return collaborator_usernames

    class Meta:
        model = Project
        fields = [
            'id', 'owner', 'profile_id', 'title', 'summary', 'collaborators', 'collaborator_usernames', 'due_date', 'complete', 'image', 'profile_image', 'created_at', 'updated_at', 'is_owner', 'is_collaborator'
        ]

    