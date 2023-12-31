from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Project
from tasks.models import Task
from django.contrib.auth.models import User


class ProjectListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing projects.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    collaborators = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(),
        required=False, read_only=False)
    collaborator_details = serializers.SerializerMethodField()
    is_collaborator = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    complete = serializers.BooleanField(read_only=True)
    completed_task_count = serializers.SerializerMethodField()
    uncompleted_task_count = serializers.SerializerMethodField()

    def validate_image(self, value):
        """
        Validate image size and dimensions.
        """
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!')
        return value

    def get_is_owner(self, obj):
        """
        Check if the current user is the owner.
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_collaborator_details(self, obj):
        """
        Get details of collaborators.
        """
        collaborators = obj.collaborators.all()
        return [{
            'id': collaborator.id,
            'collaborator_username': collaborator.username
        } for collaborator in collaborators]

    def get_is_collaborator(self, obj):
        """
        Check if the current user is a collaborator.
        """
        request = self.context['request']
        return request.user in obj.collaborators.all()

    def get_created_at(self, obj):
        """
        Format creation time using naturaltime.
        """
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        """
        Format update time using naturaltime.
        """
        return naturaltime(obj.updated_at)

    def get_completed_task_count(self, obj):
        """
        Count completed tasks for the project.
        """
        return Task.objects.filter(project=obj, complete=True).count()

    def get_uncompleted_task_count(self, obj):
        """
        Count uncompleted tasks for the project.
        """
        return Task.objects.filter(project=obj, complete=False).count()

    class Meta:
        model = Project
        fields = [
            'id', 'owner', 'profile_id', 'title', 'summary', 'collaborators',
            'collaborator_details', 'due_date', 'complete', 'image',
            'created_at', 'updated_at', 'profile_image', 'is_owner',
            'is_collaborator', 'completed_task_count', 'uncompleted_task_count'
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for project details.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    collaborators = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(), required=False, read_only=False)
    collaborator_details = serializers.SerializerMethodField()
    is_collaborator = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    completed_tasks = serializers.SerializerMethodField()
    uncompleted_tasks = serializers.SerializerMethodField()

    def validate_image(self, value):
        """
        Validate image size and dimensions.
        """
        if value.size > 1024 * 1024 * 2:
            raise serializers.ValidationError('Image size larger than 2MB!')
        if value.image.width > 4096:
            raise serializers.ValidationError(
                'Image width larger than 4096px!')
        if value.image.height > 4096:
            raise serializers.ValidationError(
                'Image height larger than 4096px!')
        return value

    def get_is_owner(self, obj):
        """
        Check if the current user is the owner.
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_collaborator_details(self, obj):
        """
        Get details of collaborators.
        """
        collaborators = obj.collaborators.all()
        return [{
            'id': collaborator.id,
            'collaborator_username': collaborator.username
        } for collaborator in collaborators]

    def get_is_collaborator(self, obj):
        """
        Check if the current user is a collaborator.
        """
        request = self.context['request']
        return request.user in obj.collaborators.all()

    def get_completed_tasks(self, obj):
        """
        Get details of completed tasks in the project.
        """
        request = self.context['request']
        tasks = Task.objects.filter(project=obj, complete=True)

        task_data = []

        for task in tasks:
            is_owner = task.owner == request.user
            is_collaborator = request.user in task.collaborators.all()

            task_data.append({
                'id': task.id,
                'name': task.title,
                'is_owner': is_owner,
                'is_collaborator': is_collaborator,
            })
        return task_data

    def get_uncompleted_tasks(self, obj):
        """
        Get details of uncompleted tasks in the project.
        """
        request = self.context['request']
        tasks = Task.objects.filter(project=obj, complete=False)

        task_data = []

        for task in tasks:
            is_owner = task.owner == request.user
            is_collaborator = request.user in task.collaborators.all()

            task_data.append({
                'id': task.id,
                'name': task.title,
                'is_owner': is_owner,
                'is_collaborator': is_collaborator,
            })

        return task_data

    class Meta:
        model = Project
        fields = [
            'id', 'owner', 'profile_id', 'title', 'summary', 'collaborators',
            'collaborator_details', 'due_date', 'complete', 'image',
            'profile_image', 'created_at', 'updated_at', 'is_owner',
            'is_collaborator', 'completed_tasks', 'uncompleted_tasks'
        ]
