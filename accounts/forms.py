from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, Delegate


class CustomUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    model = CustomUser
    fields = ('username', 'email', 'user_type')
    labels = {
      'username': _('اسم المستخدم'),
      'email': _('البريد الإلكتروني'),
      'user_type': _('نوع المستخدم'),
    }

class CustomUserChangeForm(UserChangeForm):
  class Meta:
    model = CustomUser
    fields = '__all__'

class DelegateForm(forms.ModelForm):
  class Meta:
    model = Delegate
    fields = '__all__'
    exclude = ('user',)
    widgets = {
      'start_date': forms.DateInput(attrs={'type': 'date'}),
      'end_date': forms.DateInput(attrs={'type': 'date'}),
    }
    labels = {
      'authorization_number': _('رقم التفويض'),
      'start_date': _('تاريخ البدء'),
      'end_date': _('تاريخ الانتهاء'),
      'is_active': _('نشط'),
      'authorization_document': _('وثيقة التفويض'),
    }

class CompanyRegistrationForm(forms.ModelForm):
  password1 = forms.CharField(label=_('كلمة المرور'), widget=forms.PasswordInput)
  password2 = forms.CharField(label=_('تأكيد كلمة المرور'), widget=forms.PasswordInput)
  class Meta:
    model = CustomUser
    fields = ('company_name', 'company_registration', 'tax_card', 'phone', 'email', 'governorate', 'address')
    labels = {
      'company_name': _('اسم الشركة'),
      'company_registration': _('السجل التجاري'),
      'tax_card': _('البطاقة الضريبية'),
      'phone': _('رقم الهاتف'),
      'email': _('البريد الإلكتروني'),
      'governorate': _('المحافظة'),
      'address': _('العنوان التفصيلي'),
    }
  def clean_password2(self):
    password1 = self.cleaned_data.get("password1")
    password2 = self.cleaned_data.get("password2")
    if password1 and password2 and password1 != password2:
      raise forms.ValidationError(_("كلمة المرور غير متطابقة"))
    return password2
  def save(self, commit=True):
    user = super().save(commit=False)
    user.set_password(self.cleaned_data["password1"])
    user.user_type = 'tenant'
    if commit:
      user.save()
    return user