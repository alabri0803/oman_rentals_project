# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    USER_TYPES = (
        ('owner', _('مالك المبنى')),
        ('investor', _('شركة مستثمرة')),
        ('tenant', _('شركة مستأجرة')),
        ('delegate', _('مفوض التوقيع')),
    )

    GOVERNORATES = (
        ('muscat', _('مسقط')),
        ('dhofar', _('ظفار')),
        ('musandam', _('مسندم')),
        ('buraimi', _('البريمي')),
        ('dakhiliyah', _('الداخلية')),
        ('north_batinah', _('شمال الباطنة')),
        ('south_batinah', _('جنوب الباطنة')),
        ('north_sharqiyah', _('شمال الشرقية')),
        ('south_sharqiyah', _('جنوب الشرقية')),
        ('dhahirah', _('الظاهرة')),
        ('wusta', _('الوسطى')),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES, verbose_name=_('نوع المستخدم'))
    phone = models.CharField(max_length=15, verbose_name=_('الهاتف'))
    company_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('اسم الشركة'))
    commercial_registration = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('السجل التجاري'))
    tax_card = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('البطاقة الضريبية'))
    governorate = models.CharField(max_length=20, choices=GOVERNORATES, verbose_name=_('المحافظة'))
    address = models.TextField(blank=True, null=True, verbose_name=_('العنوان'))
    is_verified = models.BooleanField(default=False, verbose_name=_('موثق'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    class Meta:
        verbose_name = _('مستخدم')
        verbose_name_plural = _('المستخدمون')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()} - {self.get_user_type_display()}"

class Delegate(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name=_('المستخدم'))
    authorization_number = models.CharField(max_length=50, verbose_name=_('رقم التفويض'))
    start_date = models.DateField(verbose_name=_('تاريخ البدء'))
    end_date = models.DateField(verbose_name=_('تاريخ الانتهاء'))
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    class Meta:
        verbose_name = _('مفوض')
        verbose_name_plural = _('المفوضون')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.authorization_number}"