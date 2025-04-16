# accounts/urls.py
from django.contrib.auth import views as auth_views
from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('profile/owner/', views.profile_owner, name='profile_owner'),
    path('profile/company/', views.profile_company, name='profile_company'),
    path('profile/delegate/', views.profile_delegate, name='profile_delegate'),

    path('users/', views.user_list, name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    path('delegate/add/', views.add_delegate, name='add_delegate'),

    # Password reset views
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt',
             extra_context={'title': _('استعادة كلمة المرور')}
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html',
             extra_context={'title': _('تم إرسال البريد')}
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             extra_context={'title': _('تأكيد استعادة كلمة المرور')}
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html',
             extra_context={'title': _('تم استعادة كلمة المرور')}
         ),
         name='password_reset_complete'),
]