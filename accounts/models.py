from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('owner', _('مالك المبنى')),
        ('investor', _('شركة مستثمرة')),
        ('tenant', _('شركة مستأجرة')),
        ('delegate', _('مفوض التوقيع')),
    )

    # معلومات أساسية
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, verbose_name=_('نوع المستخدم'))
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("يجب إدخال رقم هاتف صحيح بصيغة: '+968XXXXXXXX'"))
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name=_('رقم الهاتف'))

    # معلومات الشركة (للمستثمرين والمستأجرين)
    company_name = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('اسم الشركة'))
    commercial_registration = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('السجل التجاري'))
    tax_card = models.CharField(max_length=50, blank=True, null=True, verbose_name=_('البطاقة الضريبية'))
    company_address = models.TextField(blank=True, null=True, verbose_name=_('عنوان الشركة'))

    # معلومات إضافية
    is_verified = models.BooleanField(default=False, verbose_name=_('حساب موثوق'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    class Meta:
        verbose_name = _('مستخدم')
        verbose_name_plural = _('المستخدمون')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class Delegate(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='delegate_profile',
        verbose_name=_('المستخدم'))

    authorization_number = models.CharField(max_length=50, verbose_name=_('رقم التفويض'))
    start_date = models.DateField(verbose_name=_('تاريخ البدء'))
    end_date = models.DateField(verbose_name=_('تاريخ الانتهاء'))
    is_active = models.BooleanField(default=True, verbose_name=_('نشط'))
    authorization_document = models.FileField(
        upload_to='delegate_docs/',
        verbose_name=_('وثيقة التفويض'),
        help_text=_('يجب أن تكون الوثيقة موقعة ومختومة'))

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('تاريخ الإنشاء'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('تاريخ التحديث'))

    class Meta:
        verbose_name = _('مفوض')
        verbose_name_plural = _('المفوضون')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.authorization_number}"