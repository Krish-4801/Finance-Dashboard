import django_filters
from .models import Financials

class FinanceFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')

    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')

    class meta:
        model = Financials
        fields = ['type', 'category', 'start_date', 'end_date']
