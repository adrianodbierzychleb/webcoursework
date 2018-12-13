from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', "last_name", 'email']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:

        model = Profile
        fields = ['image', 'hobbies', 'birth_date', 'gender']
        widgets = {
            'birth_date' : DatePickerInput(
                options={
                    "format": "MM/DD/YYYY",
                    "showClose": True,
                    "showClear": True,
                    "viewMode": "years",
                }

            ),
        }
