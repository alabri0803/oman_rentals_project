from django.contrib.auth import views as auth_views
from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    # المصادقة
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html',
        extra_context={'title': _('تسجيل الدخول')}
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # التسجيل
    path('register/', views.register, name='register'),
    path('register/owner/', views.register_owner, name='register_owner'),
    path('register/investor/', views.register_investor, name='register_investor'),
    path('register/tenant/', views.register_tenant, name='register_tenant'),
    path('register/delegate/', views.register_delegate, name='register_delegate'),

    # الملفات الشخصية
    path('profile/', views.profile, name='profile'),
    path('profile/owner/<int:pk>/', views.profile_owner, name='profile_owner'),
    path('profile/investor/<int:pk>/', views.profile_investor, name='profile_investor'),
    path('profile/tenant/<int:pk>/', views.profile_tenant, name='profile_tenant'),
    path('profile/delegate/<int:pk>/', views.profile_delegate, name='profile_delegate'),

    # إدارة المستخدمين
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),

    # تغيير كلمة المرور
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        extra_context={'title': _('تغيير كلمة المرور')}
    ), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html',
        extra_context={'title': _('تم تغيير كلمة المرور')}
    ), name='password_change_done'),

    # إعادة تعيين كلمة المرور
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt',
        extra_context={'title': _('إعادة تعيين كلمة المرور')}
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html',
        extra_context={'title': _('تم إرسال البريد')}
    ), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        extra_context={'title': _('تأكيد إعادة التعيين')}
    ), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html',
        extra_context={'title': _('تم إعادة التعيين')}
    ), name='password_reset_complete'),
]