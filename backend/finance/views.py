import csv
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from users.permissions import IsAdmin, IsAnalyst
from .models import Financials
from .serializers import FinanceSerializer
from .filters import FinanceFilter

# Create your views here.
class FinancialsView(viewsets.ModelViewSet):
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
        return Financials.objects.for_user(self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsAnalyst | IsAdmin]
        else:
            permission_classes = [IsAuthenticated, IsAdmin]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.updated_by = self.request.user
        instance.delete(user=self.request.user)
    
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
            record.restore(request.user)
        return Response({"detail": "Record restored successfully."}, status=status.HTTP_200_OK)
    
    @extend_schema(
        summary="Permanently delete a record",
        description="Admin only: Permanently remove a record from the database. This action cannot be undone.",
        responses={204: OpenApiResponse(description='Record permanently deleted.')}
    )
    @action(detail=True, methods=['delete'], permission_classes=[IsAuthenticated, IsAdmin])
    def hard_del(self, request, pk=None):
        record = get_object_or_404(Financials.all_objects, pk=pk)
        record.hard_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class FinancialExportCSVView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    # ['type', 'category', 'start_date', 'end_date']
    @extend_schema(
        parameters=[
            OpenApiParameter(name='type', description='string', required=False, type=str, enum=['INCOME', 'EXPENSE']),
            OpenApiParameter(name='category', description='string', required=False, type=str),
            OpenApiParameter(name='start_date', description='Format: YYYY-MM-DD', required=False, type=str),
            OpenApiParameter(name='end_date', description='Format: YYYY-MM-DD', required=False, type=str)
        ],
        responses={
            200: OpenApiResponse(
                description="CSV File Download",
                response={
                    "text/csv": {
                        "type": "string",
                        "format": "binary"
                    }
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        queryset = Financials.objects.for_user(request.user).order_by('-date', '-created_at')
        filtered_qs = FinanceFilter(request.GET, queryset=queryset).qs
        data = FinanceSerializer(filtered_qs, many=True).data

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="financials.csv"'

        writer = csv.writer(response)
        if data:
            writer.writerow(data[0].keys())
            for item in data:
                row = []
                for key, value in item.items():
                    if key=='amount':
                        row.append(float(value))
                    else:
                        row.append(value)
                writer.writerow(row)

        return response

