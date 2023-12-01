from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Project
from .serializers import ProjectListSerializer, ProjectDetailSerializer
from drf_api.permissions import IsOwnerOrReadOnly

class ProjectList(APIView):
    """
    Lists all projects.
    """
    serializer_class = ProjectListSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly
    ]


    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectListSerializer(projects, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectListSerializer(
            data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProjectDetail(APIView):
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]
    
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