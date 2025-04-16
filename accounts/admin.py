from django import forms
from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from .models import CustomUser, Delegate


class CustomUserCreationForm(UserCreationForm):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message=_("يجب إدخال رقم هاتف صحيح بصيغة: '+968XXXXXXXX'"))

    phone = forms.CharField(
        validators=[phone_regex],
        max_length=17,
        widget=forms.TextInput(attrs={'placeholder': '+968XXXXXXXX'}),
        label=_('رقم الهاتف'))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + (
            'phone', 'user_type', 'email', 'first_name', 'last_name'
        )
        labels = {
            'user_type': _('نوع المستخدم'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

admin.site.register(CustomUser, CustomUserCreationForm, CustomUserChangeForm)
admin.site.register(Delegate, DelegateForm)