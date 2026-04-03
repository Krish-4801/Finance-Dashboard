from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import DashboardService
from drf_spectacular.utils import extend_schema, OpenApiParameter

# Create your views here.

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(
        parameters=[
            OpenApiParameter(name='start_date', description='Format: YYYY-MM-DD', required=False, type=str),
            OpenApiParameter(name='end_date', description='Format: YYYY-MM-DD', required=False, type=str),
            OpenApiParameter(name='recents', description='Number', required=False, type=int),
        ],
        responses={200:dict}
    )
    def get(self, request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        recents = request.query_params.get("recents")
        data = DashboardService.get_dashboard_data(start_date=start_date, end_date=end_date, recents=recents)
        return Response(data)
