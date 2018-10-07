from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from rest_framework import generics
from rest_framework import permissions
from rest_framework.authentication import get_authorization_header
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes, authentication_classes
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
    print(type(request.data))
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


EMAIL = {'email'}
TOKEN_PASSWORD = {'token', 'password'}
PASSWORD = {'password'}


@api_view(['PUT'])
@authentication_classes(tuple())
@permission_classes(tuple())
def password(request):
    if request.data.keys() == EMAIL:
        try:
            user = User.objects.get(email=request.data.get('email'))
        except User.DoesNotExist:
            return Response({'error': 'bad email'}, status=status.HTTP_400_BAD_REQUEST)
        new_pass = get_random_string()
        user.set_password(new_pass)
        send_mail(
            'Reset passowrd',
            'Your new password is ' + new_pass + ' please change it',
            'source_email@email.com',
            [user.email],
            fail_silently=False
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.data.keys() == TOKEN_PASSWORD:
        print("11")
        token_key = request.data.get('token')

    elif request.data.keys() == PASSWORD:
        print("22")
        auth = get_authorization_header(request).split()
        if len(auth) != 2:
            return Response({'error': 'bad authorization header'}, status=status.HTTP_400_BAD_REQUEST)
        token_key = auth[1].decode()



    else:
        return Response(
            data={
                'error': 'the body should be one of ' + ' '.join(map(
                    str,
                    (EMAIL, PASSWORD, TOKEN_PASSWORD) 
                    ))
            },
            status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.filter(auth_token__key=token_key).first()
    if user is None:
        return Response({'error': 'bad token'}, status=status.HTTP_400_BAD_REQUEST)
    user.set_password(request.data.get('password'))
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)
