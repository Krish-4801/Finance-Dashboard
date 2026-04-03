from django.db import models
from django.utils import timezone
from django.conf import settings

class ActiveFinanceMngr(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
    
    def for_user(self, user):
        if user.is_authenticated and user.role=='ADMIN':
            return Financials.all_objects.all()
        return self.get_queryset()

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
    is_deleted = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,related_name="created_financials")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="updated_financials")

    objects = ActiveFinanceMngr()
    all_objects = models.Manager()

    def __str__(self):
        return f'{self.date} - {self.type} - {self.category}: ${self.amount}'
    
    def delete(self, using = None, keep_parents = None):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at'])

    