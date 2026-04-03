from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FinancialsView, FinancialExportCSVView

router = DefaultRouter()
router.register(r'records', FinancialsView, basename='Financials')

urlpatterns = [
    path('', include(router.urls)),
    path('downloads/', FinancialExportCSVView.as_view(), name='export-csv')
]

