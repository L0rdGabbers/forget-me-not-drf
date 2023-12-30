from django.contrib.humanize.templatetags.humanize import naturaltime
from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from projects.models import Project


class TaskListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing tasks.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    collaborators = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(),
        required=False, read_only=False)
    collaborator_details = serializers.SerializerMethodField()
    is_collaborator = serializers.SerializerMethodField()
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())
    project_title = serializers.SerializerMethodField()
    complete = serializers.BooleanField(read_only=True)

    def get_is_owner(self, obj):
        """
        Check if the current user is the owner of the task.
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_is_collaborator(self, obj):
        """
        Check if the current user is a collaborator on the task.
        """
        request = self.context['request']
        return request.user in obj.collaborators.all()

    def get_collaborator_details(self, obj):
        """
        Get details of collaborators on the task.
        """
        collaborators = obj.collaborators.all()
        return [{
            'id': collaborator.id,
            'collaborator_username': collaborator.username
        } for collaborator in collaborators]

    def get_project_title(self, obj):
        """
        Get the title of the associated project.
        """
        return obj.project.title

    def get_created_at(self, obj):
        """
        Get the natural language representation of the creation time.
        """
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        """
        Get the natural language representation of the last update time.
        """
        return naturaltime(obj.updated_at)

    def get_completed_tasks(self, obj):
        """
        Get details of completed tasks associated with the project.
        """
        completed_tasks = Task.objects.filter(project=obj, complete=True)
        task_serializer = TaskSerializer(completed_tasks, many=True)
        return task_serializer.data

    def validate_project(self, value):
        """
        Validate the associated project to ensure the user is the owner.
        """
        request = self.context['request']
        if value.owner != request.user:
            raise serializers.ValidationError(
                "You can only set the project to one where you are the owner.")
        return value

    class Meta:
        model = Task
        fields = [
            'id', 'owner', 'project', 'project_title',
            'title', 'summary', 'collaborators', 'collaborator_details',
            'due_date', 'importance', 'complete',
            'created_at', 'updated_at', 'is_owner', 'is_collaborator'
        ]


class TaskDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for detailed view of a task.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())
    is_owner = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    collaborators = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all(),
        required=False, read_only=False)
    is_collaborator = serializers.SerializerMethodField()
    collaborator_details = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        """
        Check if the current user is the owner of the task.
        """
        request = self.context['request']
        return request.user == obj.owner

    def get_is_collaborator(self, obj):
        """
        Check if the current user is a collaborator on the task.
        """
        request = self.context['request']
        return request.user in obj.collaborators.all()

    def get_collaborator_details(self, obj):
        """
        Get details of collaborators on the task.
        """
        collaborators = obj.collaborators.all()
        return [{
            'id': collaborator.id,
            'collaborator_username': collaborator.username
        } for collaborator in collaborators]

    class Meta:
        model = Task
        fields = [
            'id', 'owner', 'profile_id', 'project', 'title', 'summary',
            'collaborators', 'collaborator_details', 'due_date',
            'importance', 'complete', 'created_at',
            'updated_at', 'is_owner', 'is_collaborator'
        ]
