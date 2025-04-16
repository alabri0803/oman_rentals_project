from django.db import models

from accounts.models import CustomUser


class Property(models.Model):
  PROPERTY_TYPES = (
    ('commercial', 'تجاري'),
  )
  name = models.CharField(max_length=100)
  address = models.TextField()
  city = models.CharField(max_length=50)
  governorate = models.CharField(max_length=50)
  property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
  total_area = models.DecimalField(max_digits=10, decimal_places=2)
  owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'owner'})
  investors = models.ManyToManyField(CustomUser, related_name='invested_properties', limit_choices_to={'user_type': 'investor'}, blank=True)
  description = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Unit(models.Model):
  UNIT_TYPES = (
    ('shop', 'محل'),
    ('office', 'مكتب'),
    ('apartment', 'شقة'),
    ('storge', 'مخزن'),
    ('parking', 'موقف سيارات')
  )
  property = models.ForeignKey(Property, on_delete=models.CASCADE)
  unit_type = models.CharField(max_length=20, choices=UNIT_TYPES)
  unit_number = models.CharField(max_length=50)
  area = models.DecimalField(max_digits=10, decimal_places=2)
  monthly_rent = models.DecimalField(max_digits=10, decimal_places=2)
  is_available = models.BooleanField(default=True)
  features = models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)