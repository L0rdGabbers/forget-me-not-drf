from django.http import Http404
from django.core.exceptions import ValidationError
from rest_framework import status, generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Project
from django.db.models import Q
from .serializers import ProjectListSerializer, ProjectDetailSerializer
from drf_api.permissions import (
    IsOwnerOrCollaborator, IsOwnerOrCollaboratorReadOnly)


class ProjectList(generics.ListCreateAPIView):
    """
    API view for listing and creating projects.
    """
    serializer_class = ProjectListSerializer
    permission_classes = [IsOwnerOrCollaborator, permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', ]
    ordering_fields = ['owner', 'due_date', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Get the queryset for listing projects
        based on the user's ownership or collaboration.
        """
        queryset = Project.objects.filter(
            Q(owner=self.request.user) | Q(collaborators=self.request.user)
        ).distinct()

        return queryset

    def perform_create(self, serializer):
        """
        Perform project creation and set the owner to the current user.
        """
        serializer.save(owner=self.request.user)

    def post(self, request, *args, **kwargs):
        """
        Handle HTTP POST request for creating a project.
        """
        return self.create(request, *args, **kwargs)


class ProjectDetail(APIView):
    """
    API view for retrieving, updating, and deleting a specific project.
    """
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsOwnerOrCollaboratorReadOnly]

    def get_object(self, pk):
        """
        Get the project object based on the provided primary key (pk).
        """
        try:
            project = Project.objects.get(pk=pk)
            self.check_object_permissions(self.request, project)
            return project
        except Http404:
            return Response(
                {"detail": "Project not found."},
                status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        """
        Handle HTTP GET request for retrieving a project.
        """
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(
            project, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Handle HTTP PUT request for updating a project.
        """
        try:
            project = self.get_object(pk)
            if request.user != project.owner:
                return Response(
                    {"detail": "You are not authorised to edit this project."},
                    status=status.HTTP_403_FORBIDDEN)

            serializer = ProjectDetailSerializer(
                project, data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Http404:
            return Response(
                {"detail": "Project not found."},
                status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        """
        Handle HTTP DELETE request for deleting a project.
        """
        try:
            project = self.get_object(pk)
            if request.user != project.owner:
                return Response(
                    {"detail": "You may not delete this project."},
                    status=status.HTTP_403_FORBIDDEN)

            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Http404:
            return Response(
                {"detail": "Project not found."},
                status=status.HTTP_404_NOT_FOUND)
