from django.db import models

# Create your models here.
class Financials(models.Model):
    class Type(models.TextChoices):
        INCOME = "INCOME", "Income"
        EXPENSE = "EXPENSE", "Expense"
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=Type.choices)
    category = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.date} - {self.type} - {self.category}: ${self.amount}'
