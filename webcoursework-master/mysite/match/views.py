from django.shortcuts import render, redirect
from .forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from .models import Profile

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


def list_profiles(request):
    #today = timezone.now().date()
    queryset = Profile.objects.all()
    qgender = request.GET.get("querygender")
    qminage = request.GET.get("queryagemin")
    qmaxage = request.GET.get("queryagemax")
    if qgender or qminage or qmaxage:
        queryset = queryset.filter(
            gender__icontains=qgender,
            birth_date__range=[qminage, qmaxage]
            ).distinct()
    context = {
        "object_list": queryset
    }

    return render(request, "match/list_profiles.html", context)
