from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from .serializers import CustomRegisterSerializer, UserSerializer
from .permissions import IsSuperUser

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsSuperUser]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CustomRegisterSerializer
        return UserSerializer

    def perform_create(self, serializer):
        try:
            serializer.save()
        except ValueError as e:
            raise ValidationError({"password": str(e)})
        except ValidationError as e:
            raise ValidationError({"detail": str(e)})
