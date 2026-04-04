from rest_framework import serializers

class DashboardSerializer(serializers.Serializer):
    recents = serializers.IntegerField(required=False, min_value=1, max_value=10)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)