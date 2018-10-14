from rest_framework import serializers
from .models import ProxyUser as User


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'is_superuser',
            'is_active',
            'id'
            # ...
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'email': {'read_only': True}
        }
    

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            # TODO change username as email
            'password',
            'email',
            'last_name',
            'id',
            'is_superuser',
            'is_active',
            'first_name'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'email': {'required': True}
        }


class AfterLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='auth_token.key')
    class Meta:
        model = User
        fields = (
            'token',
            'email',
            'first_name',
            'last_name',
            'is_superuser',
            'is_active',
            'id'
        )
