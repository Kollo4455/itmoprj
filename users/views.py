from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm


def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/app/predict')
        return render(request, 'users/login.html', {'form': LoginForm()})

    elif request.method == 'POST':
        form = LoginForm(request.POST)

        if not form.is_valid():
            # either form not valid or user is not authenticated
            messages.error(request, f'Invalid username or password')
            return render(request, 'users/login.html', {'form': form})

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Hi {username.title()}, welcome back!')
            return redirect('/app/predict/')


def sign_out(request):
    logout(request)
    messages.success(request, f'You have been logged out.')
    return redirect('/users/login/')


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'users/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if not form.is_valid():
            return render(request, 'users/register.html', {'form': form})

        user = form.save(commit=False)
        user.username = user.username.lower()
        user.save()
        messages.success(request, 'You have singed up successfully.')
        login(request, user)
        return redirect('/users/login/')

