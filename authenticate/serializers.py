from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'id'
            # ...
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True},
            'username': {'read_only': True}
        }
    

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            # TODO change username as email
            'password',
            'username',
            'last_name',
            'id',
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }
    

