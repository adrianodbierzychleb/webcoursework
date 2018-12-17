import django.contrib
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from datetime import date
import datetime
from datetime import timedelta


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            django.contrib.messages.success(request, f'Account created for {username}!')
            return redirect('login')
        else:
            django.contrib.messages.warning(request, f'Failed to create account')
    return render(request, 'match/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':

        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            django.contrib.messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'match/profile.html', context)


@login_required
def match(request):
    username = request.user.username
    all_users = User.objects.exclude(username=username).exclude(
        username="admin")  # all users excluding the logged in user and admin
    # all_users = dob_to_age(all_users)
    user_list = get_sorted_matched_hobbies(username, all_users)
    context = {"user_list": user_list}
    return render(request, 'match/matches.html', context)


@login_required
def filtering(request):
    if request.method == "GET":
        try:
            min_age = int(request.GET["minAge"])
        except:
            min_age = 18;
        try:
            max_age = int(request.GET["maxAge"])
        except:
            max_age = 100;

        gender = request.GET["gender"]
        username = request.user.username
        #exclude the admin profile and the user itself
        filtered_users = User.objects.exclude(username=username).exclude(username="admin")

        if gender != "None":
            filtered_users = filtered_users.filter(profile__gender=gender)
        if min_age is not None:
            min_age = calculate_dob(min_age)
            filtered_users = filtered_users.filter(profile__birth_date__lt=min_age)
        if max_age is not None:
            max_age = calculate_dob(max_age)
            filtered_users = filtered_users.filter(profile__birth_date__gt=max_age)
        #finding matched hobbies
        filtered_users = get_sorted_matched_hobbies(username, filtered_users)

        match_list = []
        #creating a list of dict to send back in json
        for entry in filtered_users:
            dict = {}
            dict["image"] = entry["user"].profile.image.url
            dict["username"] = entry["user"].username
            dict["email"] = entry["user"].email
            dict["hobbies"] = list(entry["user"].profile.hobbies.values_list("name"))
            dict["age"] = entry["user"].profile.birth_date
            match_list.append(dict)

        return JsonResponse(match_list, safe=False)

#counts how many matching hobbies and sorts in descending order
def get_sorted_matched_hobbies(username, all_users):
    user_object = User.objects.get(username=username)  # user object
    user_hobbies = list(user_object.profile.hobbies.values_list("name"))  # list of logged in user hobbies
    user_list = []
    for u in all_users:
        hobbies = list(u.profile.hobbies.values_list("name"))
        u.profile.birth_date = calculate_age(u.profile.birth_date)
        matched_hobbies = count_matching_hobbies(user_hobbies, hobbies)
        user_list.append({"user": u, "matched_hobbies": matched_hobbies})

    return sorted(user_list, key=lambda k: k['matched_hobbies'], reverse=True)

#counts the matching hobbies
def count_matching_hobbies(user_hobbies, hobbies):
    count = 0
    for h in user_hobbies:
        if h in hobbies:
            count += 1
            hobbies.remove(h)

    return count

#date to DOB
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

#DOB t date
def calculate_dob(age):
    age = age * 365.25
    return datetime.datetime.now() - timedelta(days=age)
