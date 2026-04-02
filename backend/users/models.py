from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

# Create your models here.
class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        ANALYST = 'ANALYST', 'Analyst'
        VIEWER = 'VIEWER', 'Viewer'
    
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.VIEWER)
    

    def __str__(self):
        return f"{self.username} - {self.role}"