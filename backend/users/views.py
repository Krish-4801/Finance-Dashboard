from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
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
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        user = self.get_object
        user.is_active = not user.is_active
        user.save()
        return Response({"status": f"User is now {'active' if user.is_active else 'inactive'}"})
