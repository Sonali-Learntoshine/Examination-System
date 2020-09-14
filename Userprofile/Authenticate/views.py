from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm, ProfileDetailForm
from django.contrib.auth.views import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


def dashboard(request):
    return render(request, 'dashboard.html')


def profile_detail(request):
    form = ProfileDetailForm()
    if request.method == "POST":
        form = ProfileDetailForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponse("form saved")
    return render(request, 'profile_detail.html', {'form': form})


def register_user(request):
    form = SignupForm()
    if request.method == 'POST':
        if 'login' in request.POST:
            return redirect('login')
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created for ' + username)
            return redirect('login')
        else:
            messages.error(request, 'Please Enter valid credentials')
            return redirect('signup')
    return render(request, 'accounts/signup.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'teacher_index.html', {'user': user})
        else:
            messages.error(request, 'Incorrect Username or Password')
            return redirect('login')
    return render(request, 'accounts/login.html')


def logout_user(request):
    logout(request)
    return redirect('dashboard')


def change_password(request):
    form = PasswordChangeForm(None)
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password Changed')
            return redirect('teacher:view_course')
        else:
            messages.error(request, 'Be sure about the credentials')

    return render(request, 'accounts/change_password.html', {'form': form})
