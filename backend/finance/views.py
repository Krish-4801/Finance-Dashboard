from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse

from users.permissions import IsAdmin, IsAnalyst
from .models import Financials
from .serializers import FinanceSerializer
from .filters import FinanceFilter

# Create your views here.
class FinancialsView(viewsets.ModelViewSet):
    queryset = Financials.objects.all().order_by('-date', '-created_at')
    allqueryset = Financials.all_objects.all().order_by('-date', '-created_at')

    serializer_class = FinanceSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    filterset_class = FinanceFilter

    search_fields = ['category', 'description']

    ordering_fields = ['amount', 'date', 'created_at']
    ordering = ['-date', '-created_at']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == 'ADMIN':
            return self.allqueryset
        return self.queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsAnalyst | IsAdmin]
        else:
            permission_classes = [IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]
    
    @extend_schema(
            summary="Restore a deleted record",
            description="Admin only: Restore a previously soft-deleted financial record back to active status.",
            request=None,
            responses={
                200: OpenApiResponse(description='Record restored successfully.'),
            400: OpenApiResponse(description='This record is not deleted.')
            }
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
    def restore(self, request, pk=None):
        record = get_object_or_404(Financials.all_objects, pk=pk)
        if not record.is_deleted:
            return Response({"detail": "This record is not deleted."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            record.restore()
        return Response({"detail": "Record restored successfully."}, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Permanently delete a record",
        description="Admin only: Permanently remove a record from the database. This action cannot be undone.",
        responses={204: OpenApiResponse(description='Record permanently deleted.')}
    )
    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated, IsAdmin])
    def hard_del(self, request, pk=None):
        record = get_object_or_404(Financials.all_objects, pk=pk)
        record.hard_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)