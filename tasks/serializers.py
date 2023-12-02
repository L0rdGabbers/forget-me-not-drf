from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class TaskListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    is_collaborator = serializers.SerializerMethodField()
    complete = serializers.BooleanField(read_only=True)
    file = serializers.FileField(write_only=True, allow_empty_file=True, use_url=False)

    def validate_file(self, value):
        max_size = 2 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError('File size exceeds the limit of 2MB.')
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_is_collaborator(self, obj):
        request = self.context['request']
        return request.user in obj.collaborators.all()

    class Meta:
        model = Task
        fields = [
            'id', 'owner', 'title', 'summary', 'collaborators', 'due_date', 'complete', 'file', 'created_at', 'updated_at', 'is_owner', 'is_collaborator'
        ]

class TaskDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    is_collaborator = serializers.SerializerMethodField()
    file = serializers.FileField(write_only=True, allow_empty_file=True, use_url=False)

    def validate_file(self, value):
        max_size = 2 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError('File size exceeds the limit of 2MB.')
        return value

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    def get_is_collaborator(self, obj):
        request = self.context['request']
        return request.user in obj.collaborators.all()

    class Meta:
        model = Task
        fields = [
            'id', 'owner', 'title', 'summary', 'collaborators', 'due_date', 'complete', 'file', 'created_at', 'updated_at', 'is_owner', 'is_collaborator'
        ]