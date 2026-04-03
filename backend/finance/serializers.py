from rest_framework import serializers
from datetime import date
from .models import Financials

class FinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Financials
        fields = ['id', 'amount', 'type', 'category', 'date', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_amount(self, value):
        if value<0:
            raise serializers.ValidationError("Amount must be greater than zero")
        return value
    
    def validate(self, data):
        if 'date' in data and data['date']>date.today():
            raise serializers.ValidationError(f"{data['date']}: Transaction cannot be made in future")
        return data
