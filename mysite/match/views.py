from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse

def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            messages.warning(request, f'Failed to create account')
    return render(request, 'match/register.html', {'form': form})

@login_required
def profile(request):
    
    return render(request, 'match/profile.html')
