from django.contrib.humanize.templatetags.humanize import naturaltime, naturalday
from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Project
from tasks.models import Task
from django.contrib.auth.models import User

class ProjectListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    collaborators = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False, read_only=False)
    is_collaborator = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    complete = serializers.BooleanField(read_only=True)
    completed_task_count = serializers.SerializerMethodField()
    uncompleted_task_count = serializers.SerializerMethodField()

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

    def get_created_at(self, obj):
        return naturaltime(obj.created_at)

    def get_updated_at(self, obj):
        return naturaltime(obj.updated_at)

    def get_completed_task_count(self, obj):
        return Task.objects.filter(project=obj, complete=True).count()

    def get_uncompleted_task_count(self, obj):
        return Task.objects.filter(project=obj, complete=False).count()

    class Meta:
        model = Project
        fields = [
            'id', 'owner', 'profile_id', 'title', 'summary', 'collaborators', 'due_date', 'complete', 'image',
            'created_at', 'updated_at', 'profile_image', 'is_owner', 'is_collaborator',
            'completed_task_count', 'uncompleted_task_count'
        ]

class ProjectDetailSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    collaborators = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=False)
    collaborator_usernames = serializers.SerializerMethodField()
    is_collaborator = serializers.SerializerMethodField()
    profile_id = serializers.ReadOnlyField(source='owner.profile.id')
    profile_image = serializers.ReadOnlyField(source='owner.profile.image.url')
    completed_tasks = serializers.SerializerMethodField()
    uncompleted_tasks = serializers.SerializerMethodField()

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

    def get_completed_tasks(self, obj):
        tasks = Task.objects.filter(project=obj, complete=True)
        task_data = [{'id': task.id, 'name': task.title} for task in tasks]
        return task_data

    def get_uncompleted_tasks(self, obj):
        tasks = Task.objects.filter(project=obj, complete=False)
        task_data = [{'id': task.id, 'name': task.title} for task in tasks]
        return task_data

    class Meta:
        model = Project
        fields = [
            'id', 'owner', 'profile_id', 'title', 'summary', 'collaborators', 'collaborator_usernames',
            'due_date', 'complete', 'image', 'profile_image', 'created_at', 'updated_at',
            'is_owner', 'is_collaborator', 'completed_tasks', 'uncompleted_tasks'
        ]

    