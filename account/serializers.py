from django.contrib.auth.models import User
from .models import Profile
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'date_joined']
        # 'is_staff', 'is_active', 'is_superuser', 'last_login', 'groups', 'user_permissions'
        extra_kwargs = {
            'username': {'read_only': True},
            'email': {'read_only': True},
            'date_joined': {'read_only': True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user', 'google_id', 'picture', 'bio', 'website']
        extra_kwargs = {
            'google_id': {'read_only': True},
            'picture': {'read_only': True},
            'user': {'read_only': True, 'required': False},
        }
        depth = 1


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ProfileUpdateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), required=False)

    class Meta:
        model = Profile
        fields = ['user', 'bio', 'website']
