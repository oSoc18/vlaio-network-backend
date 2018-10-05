from rest_framework import generics
from rest_framework import permissions

from .serializers import ProfileSerializer
from .permissions import SelfPermission


class Profile(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, SelfPermission)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user
