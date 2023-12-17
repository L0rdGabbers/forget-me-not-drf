from django.http import Http404
from rest_framework import status, generics,  permissions, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskListSerializer, TaskDetailSerializer
from drf_api.permissions import IsOwnerOrCollaborator
from django.db.models import Q

class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskListSerializer
    permission_classes = [IsOwnerOrCollaborator, permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['due_date', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Task.objects.filter(
            Q(owner=self.request.user) | Q(collaborators=self.request.user)
        ).distinct()

        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class TaskDetail(APIView):
    serializer_class = TaskDetailSerializer
    permission_classes = [IsOwnerOrCollaborator, permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            task = Task.objects.get(pk=pk)
            self.check_object_permissions(self.request, task)
            return task
        except:
            raise Http404
    
    def get(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskDetailSerializer(task, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        serializer = TaskDetailSerializer(task, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        task = self.get_object(pk)
        task.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )