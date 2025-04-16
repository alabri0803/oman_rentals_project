# accounts/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, DelegateForm
from .models import CustomUser, Delegate


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, _('تم تسجيل الحساب بنجاح!'))
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, _('تم تسجيل الدخول بنجاح!'))
            return redirect('dashboard')
        else:
            messages.error(request, _('اسم المستخدم أو كلمة المرور غير صحيحة'))
    return render(request, 'accounts/login.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, _('تم تسجيل الخروج بنجاح!'))
    return redirect('home')

@login_required
def profile_owner(request):
    return render(request, 'accounts/profile_owner.html', {'user': request.user})

@login_required
def profile_company(request):
    return render(request, 'accounts/profile_company.html', {'user': request.user})

@login_required
def profile_delegate(request):
    delegate = get_object_or_404(Delegate, user=request.user)
    return render(request, 'accounts/profile_delegate.html', {'delegate': delegate})

@login_required
def user_list(request):
    users = CustomUser.objects.all()
    return render(request, 'accounts/user_list.html', {'users': users})

@login_required
def user_detail(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    return render(request, 'accounts/user_detail.html', {'user': user})

@login_required
def add_delegate(request):
    if request.method == 'POST':
        form = DelegateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('تم إضافة المفوض بنجاح!'))
            return redirect('user_list')
    else:
        form = DelegateForm()
    return render(request, 'accounts/add_delegate.html', {'form': form})