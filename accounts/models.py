from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
  USER_TYPES = (
    ('owner', 'مالك المبني'),
    ('investor', 'شركة مستثمر'),
    ('tenant', 'شركة مستأجر'),
    ('delegate', 'مفوض التوقيع')
  )
  user_type = models.CharField(max_length=10, choices=USER_TYPES)
  phone_number = models.CharField(max_length=15, blank=True, null=True)
  company_name = models.CharField(max_length=100, blank=True, null=True)
  company_registration = models.CharField(max_length=50, blank=True, null=True)
  tax_card = models.CharField(max_length=50, blank=True, null=True)

class Delegate(models.Model):
  user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
  authorization = models.CharField(max_length=50)
  start_date = models.DateField()
  end_date = models.DateField()
  is_active = models.BooleanField(default=True)