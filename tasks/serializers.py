from django.contrib.humanize.templatetags.humanize import naturaltime
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

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    def get_completed_tasks(self, obj):
        completed_tasks = Task.objects.filter(project=obj, complete=True)
        task_serializer = TaskSerializer(completed_tasks, many=True)
        return task_serializer.data

    def validate_project(self, value):
        request = self.context['request']
        if value.owner != request.user:
            raise serializers.ValidationError("You can only set the project to one where you are the owner.")
        return value

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
    collaborator_usernames = serializers.SerializerMethodField()

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
        model = Task
        fields = [
            'id', 'owner', 'project', 'title', 'summary', 'collaborators', 'collaborator_usernames', 'due_date', 'complete', 'created_at', 'updated_at', 'is_owner', 'is_collaborator'
        ]
