from django.http import Http404
from rest_framework import status, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly

class ProfileList(generics.ListAPIView):
    """
    Lists all user profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['owner__username',]

    
class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer