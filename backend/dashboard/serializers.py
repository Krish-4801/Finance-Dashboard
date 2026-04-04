from rest_framework import serializers

# serializer for input for dashboad
class DashboardSerializer(serializers.Serializer):
    recents = serializers.IntegerField(required=False, min_value=1, max_value=10)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

# Serializers for apidocs
class OverviewSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=10, decimal_places=2)
    net_balance = serializers.DecimalField(max_digits=10, decimal_places=2)

class MonthlyTrendSerializer(serializers.Serializer):
    month = serializers.CharField()
    type = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_Count = serializers.IntegerField()

class WeeklyTrendSerializer(serializers.Serializer):
    week = serializers.CharField()
    type = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)
    transaction_Count = serializers.IntegerField()

class CategoryTotalSerializer(serializers.Serializer):
    category = serializers.CharField()
    type = serializers.CharField()
    total = serializers.DecimalField(max_digits=10, decimal_places=2)

class DashboardResponseSerializer(serializers.Serializer):
    overview = OverviewSerializer()
    category_total = CategoryTotalSerializer(many=True)
    monthly_trends = MonthlyTrendSerializer(many=True)
    weekly_trends = WeeklyTrendSerializer(many=True)
    recent_activities = serializers.ListField()