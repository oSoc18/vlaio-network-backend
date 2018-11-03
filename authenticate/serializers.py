from django.utils.crypto import get_random_string
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
            'role',
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
            'email',
            'last_name',
            'id',
            'role',
            'first_name'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'email': {'required': True}
        }
    
    def create(self, validated_data):
        validated_data['password'] = get_random_string()
        return super().create(validated_data)


class AfterLoginSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='auth_token.key')
    class Meta:
        model = User
        fields = (
            'token',
            'email',
            'first_name',
            'last_name',
            'role',
            'id'
        )
