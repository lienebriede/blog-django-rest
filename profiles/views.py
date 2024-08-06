from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from blog_api.permissions import IsOwnerOrReadOnly

class ProfileList(APIView):
    """
    List all profiles
    Profile creation is handled by django signals
    """
    def get(self, request):
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(
            profiles, many=True, context={'request': request}
            ) # access request object in serializer (every time we call it)
        return Response(serializer.data)

class ProfileDetail(APIView):
    serializer_class = ProfileSerializer #renders a form for the editing
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        profile = self.get_object(pk)
        serializer = ProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)