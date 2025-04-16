from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView, ListView

from .forms import CustomUserCreationForm, DelegateForm
from .models import CustomUser, Delegate


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()

    return render(request, 'accounts/register.html', {
        'form': form,
        'title': _('تسجيل حساب جديد')
    })

def register_owner(request):
    return register_by_type(request, 'owner', _('تسجيل مالك مبنى'))

def register_investor(request):
    return register_by_type(request, 'investor', _('تسجيل شركة مستثمرة'))

def register_tenant(request):
    return register_by_type(request, 'tenant', _('تسجيل شركة مستأجرة'))

def register_delegate(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST, prefix='user')
        delegate_form = DelegateForm(request.POST, request.FILES, prefix='delegate')

        if user_form.is_valid() and delegate_form.is_valid():
            user = user_form.save(commit=False)
            user.user_type = 'delegate'
            user.save()

            delegate = delegate_form.save(commit=False)
            delegate.user = user
            delegate.save()

            login(request, user)
            return redirect('profile_delegate', pk=user.pk)
    else:
        user_form = CustomUserCreationForm(prefix='user')
        delegate_form = DelegateForm(prefix='delegate')

    return render(request, 'accounts/register_delegate.html', {
        'user_form': user_form,
        'delegate_form': delegate_form,
        'title': _('تسجيل مفوض توقيع')
    })

def register_by_type(request, user_type, title):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = user_type
            user.save()
            login(request, user)
            return redirect(f'profile_{user_type}', pk=user.pk)
    else:
        form = CustomUserCreationForm(initial={'user_type': user_type})

    return render(request, 'accounts/register.html', {
        'form': form,
        'title': title
    })

@login_required
def profile(request):
    user = request.user
    if user.user_type == 'owner':
        return redirect('profile_owner', pk=user.pk)
    elif user.user_type == 'investor':
        return redirect('profile_investor', pk=user.pk)
    elif user.user_type == 'tenant':
        return redirect('profile_tenant', pk=user.pk)
    elif user.user_type == 'delegate':
        return redirect('profile_delegate', pk=user.pk)
    return redirect('home')

@login_required
def profile_owner(request, pk):
    user = get_object_or_404(CustomUser, pk=pk, user_type='owner')
    return render(request, 'accounts/profile_owner.html', {
        'profile_user': user,
        'title': _('ملف المالك')
    })

@login_required
def profile_investor(request, pk):
    user = get_object_or_404(CustomUser, pk=pk, user_type='investor')
    return render(request, 'accounts/profile_investor.html', {
        'profile_user': user,
        'title': _('ملف المستثمر')
    })

@login_required
def profile_tenant(request, pk):
    user = get_object_or_404(CustomUser, pk=pk, user_type='tenant')
    return render(request, 'accounts/profile_tenant.html', {
        'profile_user': user,
        'title': _('ملف المستأجر')
    })

@login_required
def profile_delegate(request, pk):
    user = get_object_or_404(CustomUser, pk=pk, user_type='delegate')
    delegate = get_object_or_404(Delegate, user=user)
    return render(request, 'accounts/profile_delegate.html', {
        'profile_user': user,
        'delegate': delegate,
        'title': _('ملف المفوض')
    })

class UserListView(ListView):
    model = CustomUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        return CustomUser.objects.all().order_by('-date_joined')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('قائمة المستخدمين')
        return context

class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'accounts/user_detail.html'
    context_object_name = 'profile_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        context['title'] = _('تفاصيل المستخدم')

        if user.user_type == 'delegate':
            context['delegate'] = Delegate.objects.get(user=user)

        return context