from rest_framework import serializers
from datetime import date
from .models import Financials

class FinanceSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    updated_by_username = serializers.CharField(source='updated_by.username', read_only=True)
    class Meta:
        model = Financials
        fields = ['id', 'amount', 'type', 'category', 'date', 'description', 'created_at', 'updated_at', 'is_deleted', 'deleted_at', 'created_by_username', 'updated_by_username']
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted', 'deleted_at', 'created_by_username', 'updated_by_username']
    
    def validate_amount(self, value):
        if value<=0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value
    
    def validate(self, data):
        if 'date' in data and data['date']>date.today():
            raise serializers.ValidationError(f"{data['date']}: Transaction cannot be made in future")
        return data
