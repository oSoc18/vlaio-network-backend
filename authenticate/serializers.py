from django.contrib.auth.models import User
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'email',
            # ...
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'read_only': True}
        }
