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

    This view returns a list of all user profiles.
    It supports ordering and search filtering.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # Specify filter backends for ordering and search
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]

    # Define fields for which search filtering is allowed
    search_fields = ['owner__username', ]


class ProfileDetail(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update a profile if you're the owner.

    This view allows users to retrieve or update their own profile.
    Only the owner of the profile has permission to update it.
    """
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
