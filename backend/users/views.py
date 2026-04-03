from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .serializers import UserSerializer, UserCreateSerializer
from .permissions import IsAdmin

User = get_user_model()
# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_serializer_class(self):
        if self.action=='create':
            return UserCreateSerializer
        return UserSerializer