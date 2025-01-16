from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'date_joined']
        # 'is_staff', 'is_active', 'is_superuser', 'last_login', 'groups', 'user_permissions'


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'google_id', 'picture', 'bio', 'website']
        extra_kwargs = {
            'google_id': {'read_only': True},
            'picture': {'read_only': True}
        }
        depth = 1
