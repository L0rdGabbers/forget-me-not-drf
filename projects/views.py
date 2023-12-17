from django.http import Http404
from django.core.exceptions import ValidationError
from rest_framework import status, generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Project
from django.db.models import Q
from .serializers import ProjectListSerializer, ProjectDetailSerializer
from drf_api.permissions import IsOwnerOrCollaboratorReadOnly, IsOwnerOrCollaborator

class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectListSerializer
    permission_classes = [IsOwnerOrCollaborator, permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title',]
    ordering_fields = ['owner', 'due_date', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Project.objects.filter(
            Q(owner=self.request.user) | Q(collaborators=self.request.user)
        ).distinct()

        return queryset

    def perform_create(self, serializer):
        collaborators_data = self.request.data.get('collaborators', [])
        try:
            collaborators = [int(collaborator_id) for collaborator_id in collaborators_data]
        except ValueError:
            return Response({"detail": "Invalid collaborator ID(s) provided."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(owner=self.request.user, collaborators=collaborators)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
class ProjectDetail(APIView):
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsOwnerOrCollaboratorReadOnly]
    
    def get_object(self, pk):
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except:
            raise Http404

    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        project = self.get_object(pk)
        project.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )