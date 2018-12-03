from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse


def index(request):
    login_form = LoginForm()
    reg_form = RegistrationForm()
    return render(request, 'match/index.html', {'login_form':login_form, 'reg_form':reg_form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect(index)
        else:
            messages.warning(request, f'Failed to create account')
        return redirect(index)


@login_required
def home(request):
    return render(request, 'match/home.html')
