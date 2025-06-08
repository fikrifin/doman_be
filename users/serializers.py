from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.contrib.auth.models import User

class CustomRegisterSerializer(RegisterSerializer):
    email = None

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', 'user_permissions', 'groups', 'is_superuser', 'last_login', 'date_joined', 'is_staff']