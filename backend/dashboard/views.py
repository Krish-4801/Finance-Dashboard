from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter, inline_serializer
from .services import DashboardService
from .serializers import DashboardSerializer, DashboardResponseSerializer

# Create your views here.

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        parameters=[
            OpenApiParameter(name='start_date', description='Format: YYYY-MM-DD', required=False, type=str),
            OpenApiParameter(name='end_date', description='Format: YYYY-MM-DD', required=False, type=str),
            OpenApiParameter(name='recents', description='Number', required=False, type=int),
        ],
        responses={200: DashboardResponseSerializer}
    )
    def get(self, request):
        serializer = DashboardSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        start_date = serializer.validated_data.get('start_date')
        end_date = serializer.validated_data.get('end_date')
        recents = serializer.validated_data.get('recents', 5)
        data = DashboardService.get_dashboard_data(start_date=start_date, end_date=end_date, recents=recents)
        return Response(data)
