from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from projects.models import Project

class TaskListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    collaborators = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    collaborator_usernames = serializers.SerializerMethodField()
    is_collaborator = serializers.SerializerMethodField()
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    project_title = serializers.SerializerMethodField()
    complete = serializers.BooleanField(read_only=True)

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

    def get_project_title(self, obj):
        return obj.project.title

    class Meta:
        model = Task
        fields = [
            'id', 'owner', 'project', 'project_title', 'title', 'summary', 'collaborators', 'collaborator_usernames',
            'due_date', 'importance', 'complete', 'created_at', 'updated_at', 'is_owner', 'is_collaborator'
        ]

class TaskDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    is_owner = serializers.SerializerMethodField()
    is_collaborator = serializers.SerializerMethodField()

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
            'id', 'owner', 'project', 'title', 'summary', 'collaborators', 'due_date', 'complete', 'created_at', 'updated_at', 'is_owner', 'is_collaborator'
        ]
