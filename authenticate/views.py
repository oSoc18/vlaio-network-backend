from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

from .serializers import ProfileSerializer, RegisterSerializer
from .permissions import SelfPermission

User = get_user_model()


class Profile(generics.RetrieveUpdateAPIView):
    permission_classes = (permissions.IsAuthenticated, SelfPermission)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user

class LoginView(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'last_name': user.last_name,
            'first_name': user.first_name
        })


class UserViews(APIView):
    permission_classes = (permissions.IsAdminUser, )
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = ProfileSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


PATCH_FIELDS = ['is_staff', 'is_superuser', 'email']

@api_view(['PATCH', 'DELETE'])
@permission_classes((permissions.IsAdminUser, ))
def user_patch_delete(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        for field in PATCH_FIELDS:
            setattr(
                user,
                field,
                request.data.get(
                    field,
                    getattr(user, field)
            ))
        user.save()
    else:
        user.delete(id=pk)
        # user.is_active = False
        # user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
