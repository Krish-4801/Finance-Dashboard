from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from users.permissions import IsAdmin, IsAnalyst
from .models import Financials
from .serializers import FinanceSerializer
from .filters import FinanceFilter

# Create your views here.
class FinancialsView(viewsets.ModelViewSet):
    queryset = Financials.objects.all().order_by('-date', '-created_at')
    serializer_class = FinanceSerializer
    filter_backends = [DjangoFilterBackend] # need to add thnis to global later
    filterset_class = FinanceFilter

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsAnalyst | IsAdmin]
        else:
            permission_classes = [IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]