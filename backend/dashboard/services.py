from django.db.models import Sum, Q, Value, DecimalField, Count
from django.db.models.functions import Coalesce, TruncMonth, TruncWeek
from finance.models import Financials

class DashboardService:
    @staticmethod
    def get_dashboard_data(start_date=None, end_date=None, recents=None):
        # date filter
        queryset = Financials.objects.all()
        if start_date:
            queryset=queryset.filter(date__gte=start_date)
        if end_date:
            queryset=queryset.filter(date__lte=end_date)
        
        # total income and expense
        totals = queryset.aggregate(
            total_income = Coalesce(
                Sum('amount', filter=Q(type=Financials.Type.INCOME)),
                Value(0, output_field=DecimalField(max_digits=10, decimal_places=2))
            ),
            total_expense =Coalesce(
                Sum('amount', filter=Q(type=Financials.Type.EXPENSE)),
                Value(0, output_field=DecimalField(max_digits=10, decimal_places=2))
            )
        )

        total_income = totals['total_income']
        total_expense = totals['total_expense']
        net_balance = total_income-total_expense

        # Category wise total
        category_total = queryset.values('category', 'type').annotate(total=Sum('amount')).order_by('-total')

        # Monthly Trends
        month_total = queryset.annotate(month=TruncMonth('date')).values('month', 'type').annotate(total=Sum('amount'), transaction_Count=Count('id')).order_by('month')

        # Weekly trends
        week_total = queryset.annotate(week=TruncWeek('date')).values('week', 'type').annotate(total=Sum('amount'), transaction_Count=Count('id')).order_by('week')

        #Recent activities
        recent_activities = queryset.order_by('-date', '-created_at').values(
            'id', 'amount', 'type', 'category', 'date', 'description'
        )[:recents]

        return {
            "overview":{
                "total_income" : total_income,
                "total_expense" : total_expense,
                "net_balance" : net_balance
            },
            "category_total" : list(category_total),
            "monthly_trends" : [{
                "month" : trend["month"].strftime('%Y-%m'),
                "type" : trend["type"],
                "total" : trend["total"],
                "transaction_Count" : trend["transaction_Count"]
            } for trend in month_total],
            "weekly_trends" : [{
                "week" : trend["week"].strftime('%G-W%V'),
                "type" : trend["type"],
                "total" : trend["total"],
                "transaction_Count" : trend["transaction_Count"]
            } for trend in week_total],
            "recent_activities" : list(recent_activities),
        }