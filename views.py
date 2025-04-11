from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, LoginForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required, user_passes_test

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'register.html', {'form': form})

def login_view(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html', {'form': form})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

@user_passes_test(lambda u: u.role == 'Admin')
def admin_only_view(request):
    users = CustomUser.objects.all()
    return render(request, 'admin_only.html', {'users': users})

def logout_view(request):
    logout(request)
    return redirect('login')


def is_admin(user):
    return user.role == 'Admin'

@login_required
@user_passes_test(is_admin)
def admin_only(request):
    return render(request, 'admin_only.html')